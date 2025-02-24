from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, explode
from pyspark.sql.types import ArrayType, MapType, StringType
from processors.extract_pages import extract_person_pages
from consumers.base_consumer import BaseConsumer
from producers.person_producer import PersonProducer
from config.settings import CONSUMER_CONFIG

class HtmlConsumer(BaseConsumer):

    def __init__(self):
        super().__init__(topic="html_topic")
        self.producer = PersonProducer()
        self.spark = SparkSession.builder\
                .appName("HtmlConsumerSpark")\
                .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
                .getOrCreate()

    def process_message(self):
        schema = ArrayType(MapType(StringType(), StringType()))
        extract_pages_spark_udf = udf(extract_person_pages, schema)

        kafka_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", CONSUMER_CONFIG['bootstrap.servers']) \
            .option("subscribe", "html_topic") \
            .option("startingOffsets", "earliest") \
            .load()

        file_paths_df = kafka_df.selectExpr("CAST(value AS STRING) AS file_path")

        extracted_pages_df = file_paths_df.withColumn("extracted_pages", extract_pages_spark_udf("file_path"))
        flattened_df = extracted_pages_df.withColumn("page", explode("extracted_pages")) \
            .select("file_path", "page.page_title", "page.content")

        query = flattened_df.writeStream \
            .option("checkpointLocation", "/tmp/spark_checkpoint/") \
            .foreachBatch(self.process_batch) \
            .outputMode("append") \
            .start()

        query.awaitTermination(timeout=10)

    def process_batch(self, batch_df, batch_id):
        for row in batch_df.collect():
            message = {
                "file_path": row.file_path,
                "page_title": row.page_title,
                "content": row.content
            }
            self.producer.produce_person(message)