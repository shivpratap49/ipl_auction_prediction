from docutils.nodes import topic
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, BooleanType

spark=SparkSession.builder\
    .appName("setapp")\
    .config("spark.sql.shuffle.partitions","2")\
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .getOrCreate()

schema = StructType([
    StructField("info", StructType([
        StructField("satname", StringType(), True),
        StructField("satid", IntegerType(), True),
        StructField("transactionscount", IntegerType(), True)
    ]), True),
    StructField("positions", ArrayType(StructType([
        StructField("satlatitude", DoubleType(), True),
        StructField("satlongitude", DoubleType(), True),
        StructField("sataltitude", DoubleType(), True),
        StructField("azimuth", DoubleType(), True),
        StructField("elevation", DoubleType(), True),
        StructField("ra", DoubleType(), True),
        StructField("dec", DoubleType(), True),
        StructField("timestamp", IntegerType(), True),
        StructField("eclipsed", BooleanType(), True)
    ])), True)
])
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "satelite") \
    .option("startingOffsets", "latest") \
    .load()
parsed_df = df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

flattened_df = parsed_df.select(
    col("info.satname").alias("satname"),
    col("info.satid").alias("satid"),
    col("info.transactionscount").alias("transactionscount"),
    explode(col("positions")).alias("position")
).select(
    "satname",
    "satid",
    "transactionscount",
    "position.satlatitude",
    "position.satlongitude",
    "position.sataltitude",
    "position.azimuth",
    "position.elevation",
    "position.ra",
    "position.dec",
    "position.timestamp",
    "position.eclipsed"
).withColumn("timestamp", from_unixtime("timestamp"))\
    .withColumn("date",to_date("timestamp"))
query = flattened_df.writeStream \
    .outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="satellite_data", keyspace="satellite_db")\
    .option("checkpointLocation", "/tmp") \
    .start()

query.awaitTermination()