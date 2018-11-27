# playing with cloud composer
small example that sets up dataproc cluster, runs pyspark (csv2parquet converstion) and deletes cluster

convert.py - simple converstion of a test csv file sitting in GCS

cc-convert4.py - defines a DAG that creates dataproc cluster, runs conversion and deletes cluster

