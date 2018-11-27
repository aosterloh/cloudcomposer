# playing with cloud composer
small example that sets up dataproc cluster, runs pyspark (csv2parquet converstion) and deletes cluster

convert.py - simple converstion of a test csv file sitting in GCS (to test that code works) 
upload file it to GCS and reference it in the DAG

```
cc-convert4.py - defines a DAG that creates dataproc cluster, runs conversion and deletes cluster
    run_dataproc_csv2parquet = dataproc_operator.DataProcPySparkOperator(
      task_id='run_dataproc_parquetconvert',
      cluster_name='parquetconverter2',
      main='gs://alex-code/convert.py')
```
Above defines pyspark operator with a task identifier, name of cluster (that was created a step before) and the code reference

```
create_dataproc_cluster >> run_dataproc_csv2parquet >> delete_dataproc_cluster
```
Above defines dependencies 


### csv file in my case has 9 columns and looks like this

    15.0,Sun,0,-73.988204,40.748077,-74.006914,40.707128,1.0,2012-09-16 00:06:07.000000-73.988240.748140.7071-74.0069
    3.7,Sun,0,-73.988535,40.723059,-73.990247,40.729007,1.0,2010-01-31 00:47:33.000000-73.988540.723140.729-73.9902
    8.0,Sun,2,-73.989582,40.720431,-74.00426,40.722064,4.0,2014-07-20 02:20:38.000000-73.989640.720440.7221-74.0043
    10.9,Sun,3,-73.998535,40.72639,-73.987103,40.767985,5.0,2009-05-10 03:37:00.000000-73.998540.726440.768-73.9871

