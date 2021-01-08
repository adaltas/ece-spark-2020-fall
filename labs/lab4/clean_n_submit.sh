#!/bin/bash

# submit application by it's file name

# $1 = application file
# $2 = checkpoint directory
HOST="edge-1.au.adaltas.cloud"
PORT=11111

if [ "$#" -gt 0 ]; then
  appfile="$1"
  checkpointdir="${2:-/user/$USER/checkpoint}"
  outputdir="${3:-/user/$USER/streaming-output}" 
  echo $appfile
  echo $checkpointdir
  echo $outputdir
  if $(hdfs dfs -test -d ${checkpointdir}); then
    hdfs dfs -rm -r ${checkpointdir}
  fi
  if $(hdfs dfs -test -d ${outputdir}); then
    hdfs dfs -rm -r ${outputdir}
  fi
  spark-submit --master yarn \
  --deploy-mode cluster \
  "$appfile" \
  "$USER"-"$appfile" \
  "$HOST" \
  "$outputdir" \
  -f "$PORT" \
  -c "$checpointdir"  
else
  echo "Wrong parameters"
  echo "Usage: clean_n_submit.sh <appfile.py> [<checkpoint_directory>] [<output_directory>]"
fi

