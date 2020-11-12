# Structured Streaming lab

The goals of this labs are to:
- Stream the NYC Taxi datasets on a socket
- Use Spark Streaming to analyze the stream

## Lab resources

- The `data` directory contains the NYC Taxi datasets;
- The `stream_taxi_data.py` allows to stream a dataset through a socket on a given port.

## Streaming the datasets

To stream the NY datasets:
- Go to this directory:
  ```
  cd ece-spark/structured-streaming
  ```
- Run the `stream_taxi-data.py` script. The script has 3 parameters: the server name to use to stream the data, the port on which to open the socket, the dataset to stream (can be either `fares` or `rides`)
  ```
  python3 stream_taxi_data.py edge1.au.adaltas.cloud 11111 fares
  ```
