from pydantic.v1.utils import truncate
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from sqlalchemy import false
from torch.utils.hipify.hipify_python import value

spark = SparkSession.builder\
            .appName("demo06")\
            .config("spark.sql.shuffle.partitions", "2")\
            .getOrCreate()



df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "ncdc") \
.option("startingOffsets", "latest") \
  .load()
regex = r"^.{15}([0-9]{4}).{68}([-\+][0-9]{4})([0-9]).*$"
df_string = df.selectExpr("CAST(value AS STRING)") \
    .select(regexp_extract("value", regex, 1).alias("year").cast('SHORT'),\
            regexp_extract("value", regex, 2).alias("temprature").cast('SHORT'),\
            regexp_extract("value", regex, 3).alias("quality").cast('BYTE'))

query=df_string.writeStream\
    .foreach(mysql_connect.MySQLSink()) \
    .outputMode("append")\
    .start()
query.awaitTermination()

spark.stop()