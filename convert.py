from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import random, string
import datetime

if __name__ == "__main__":
    sc = SparkContext(appName="CSV2Parquet")
    sqlContext = SQLContext(sc)
    
    schema = StructType([
            StructField("col1", StringType(), True),
            StructField("col2", StringType(), True),
            StructField("col3", StringType(), True),
            StructField("col4", StringType(), True),
            StructField("col5", StringType(), True),
            StructField("col6", StringType(), True),
            StructField("col7", StringType(), True),
            StructField("col8", StringType(), True),
            StructField("col9", StringType(), True)])
    
    rdd = sc.textFile("gs://alex-staging/train.csv").map(lambda line: line.split(","))
    df = sqlContext.createDataFrame(rdd, schema)
    currentDT = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    print('Writing to ' + currentDT)
    df.write.parquet('gs://alex-staging/output/parquet/'+currentDT)
