# Data Engineering with Spark

## Lab 4: Application submitting

### Prerequisites

Connect to the Adaltas cloud cluster using OpenVPN.

### Goals

- Submit a pyspark application using `spark-submit`
- Add custom application properties to the `spark-submit`
- Use a `.properties` files to store the properties

### Lab resources

- The `taxi_streaming_analysis.py` pyspark script reads streaming data from a socket and outputs aggregated results in parquet format to a HDFS directory
- The `app.properties` file defines Spark application properties
- The `yarn_kill_app.sh` can be used to easily kill a YARN application using a keyword and a username

### Useful links

- [Spark - Submitting Applications doc](https://spark.apache.org/docs/2.3.2/submitting-applications.html)
- [Spark - Configuration doc](https://spark.apache.org/docs/2.3.2/configuration.html)
- [Spark - Structured Streaming doc](http://spark.apache.org/docs/2.3.2/structured-streaming-programming-guide.html)

### Submitting the application

- Go to the `labs/lab4` directory
- Use `spark-submit` to submit the application:
  ```sh
  spark-submit --master yarn \
  --deploy-mode cluster \
  ./taxi_streaming_analysis.py \
  APP_NAME \
  HOST_ADDRESS \
  HDFS_OUTPUT_DIRECTORY \
  -f PORT_NUMBER
  ```
  
  `APP_NAME` is a name to show in the list of running applications (you could choose it)
  
  `HDFS_OUTPUT_DIRECTORY` is a directory which will contain the results. If you work on edge server you could use relative path, for example:
  `/education/ece/big-data/2020/fall/bda/gr1/$USER/spark-lab4/output/fares_metrics` or full path `hdfs://HDFS_SERVER_HOST/education/ece/big-data/2020/fall/bda/gr1/$USER/spark-lab4/output/fares_metrics`. 
  Creation of the directory before the run is not necessarily. It will be created automatically. 
  
  `HOST_ADDRESS` and `PORT_NUMBER` show the resource of streaming data. For instance: `edge-1.au.adaltas.cloud` and `11111`.
  
- To stop the application using `yarn application`
  - Use the `-list` command to find your application:
    ```sh
    yarn application -list | grep "$USER"
    ```
  - Kill the application using the `-kill` command and the application ID:
    ```sh
    yarn application -kill APP_ID
    ```
- Before re-submitting the app, clear the output and the checkpoint directory:
  ```sh
  hdfs dfs -rm -r /HDFS_OUTPUT_DIRECTORY/*
  hdfs dfs -rm -r /user/USERNAME/checkpoint/*
  ```

### TO DO

1. Modify the `spark_taxi_streaming.py` file with your code from lab 3
2. Submit the application using `spark-submit`
3. Observe the results using Zeppelin (see `ece-2019/spark/ref/lab4` notebook)
4. Add custom application properties to the `spark-submit`
5. Write those properties in a `.properties` file
6. (Bonus) Write a bash script to automate the app submitting + directories cleaning in HDFS
7. (Bonus) Write a bash script to automate the YARN application killing
