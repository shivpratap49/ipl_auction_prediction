

from pyspark.sql import SparkSession
from pyspark.sql.functions import *



spark = SparkSession.builder \
    .appName("CassandraToHive") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .getOrCreate()

cassandra_df = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="satellite_data", keyspace="satellite_db") \
    .load()\

print("Data read from Cassandra:")
df1=cassandra_df.coalesce(1) \
    .where(expr("timestampdiff(DAY, timestamp, current_timestamp()) = 0"))


df1.write\
    .format("csv") \
    .mode("append") \
    .save("hdfs://localhost:9000/user/shiv/cassandra_data")
spark.stop()