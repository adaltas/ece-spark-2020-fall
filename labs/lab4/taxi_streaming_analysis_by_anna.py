import argparse
import getpass
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, window, count, mean, udf, col

# Use Python argparse library to parse arguments
parser = argparse.ArgumentParser(
    description='Process NYC Taxi datasets in streaming using sockets')
parser.add_argument('appname', type=str, help='The Spark application name')
parser.add_argument('sockethostname', type=str,
                    help='The hostname on which to listen to the socket')
parser.add_argument('outputpath', type=str,
                    help='The HDFS path where to write the CSV output')
parser.add_argument('-f', '--faresport', type=int, default=11111,
                    help='The port on which the fares dataset is streamed')
parser.add_argument('-r', '--ridesport', type=int, default=11112,
                    help='The port on which the rides dataset is streamed')
parser.add_argument('-c', '--checkpoint', type=str, help='The HDFS path '
                    'where Spark will write checkpointing infomation. '
                    'Default = /user/USERNAME/checkpoint/APP_NAME')

args = parser.parse_args()

print('appname = %s' % args.appname)
print('host = %s' % args.sockethostname)
print('faresport = %s' % args.faresport)
print('checkpoint path = %s' % args.checkpoint)
print('outputpath = %s' % args.outputpath)

# Create a new SparkSession
spark = ( 
    SparkSession
    .builder
    .appName(args.appname)
    .getOrCreate()
)

# Print the application Web UI url
print('Application Web UI: %s' % spark.sparkContext.uiWebUrl)

# Define UDF for the tip level
def tip_level_calc(tip, total):
    if total > 0:
        if tip == 0:
            return 'zero'
        elif tip / total < 0.05:
            return 'low'
        elif tip / total < 0.05:
            return 'low'
        elif tip / total < 0.2:
            return 'medium'
        else:
            return 'high'
    else:
        return 'error'

# Register UDF
calctiplevelUDF = udf(lambda a,b: tip_level_calc(a,b))

# Define the stream source (socket)
fares_raw = (
    spark
    .readStream
    .format("socket")
    .option("host", args.sockethostname)
    .option("port", args.faresport)
    .load()
)

# Parse the socket message "manually"
fares = fares_raw.select(
        split(fares_raw.value, ',')[0].alias('ride_id').cast('int'),
        split(fares_raw.value, ',')[1].alias('taxi_id').cast('int'),
        split(fares_raw.value, ',')[2].alias('driver_id').cast('int'),
        split(fares_raw.value, ',')[3].alias('start_time').cast('timestamp'),
        split(fares_raw.value, ',')[4].alias('payment_type'),
        split(fares_raw.value, ',')[5].alias('tip').cast('float'),
        split(fares_raw.value, ',')[6].alias('tolls').cast('float'),
        split(fares_raw.value, ',')[7].alias('total_fare').cast('float')
)

# Define the aggregation to perform on the stream
fares_count = (
    fares
    .withColumn('tip_level', calctiplevelUDF('tip','total_fare'))
    .withWatermark('start_time', '5 minutes')
    .groupBy(
        window('start_time', '2 minutes', '2 minutes'),
        col('tip_level')
    )
    .agg(
        count('ride_id').alias('ride_count'),
        mean('total_fare').alias('mean_total_fare'),
        mean('tip').alias('mean_tip')
    )
)

# Define the stream sink (parquet files written to HDFS)
# The trigger control the occurance of parquet file generation
query = (
    fares_count
    .writeStream
    .outputMode('append')
    .format('parquet')
    .trigger(processingTime='15 seconds')
    .option('path', args.outputpath)
    .option('checkpointLocation', args.checkpoint if args.checkpoint
            else '/user/{}/checkpoint/{}'.format(
                getpass.getuser(), args.appname))
    .start()
)

# Wait for the end of the query before ending the application
query.awaitTermination()

