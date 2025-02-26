from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from pyspark.sql.functions import explode, udf, col
from processors.extract_pages import extract_pages_spark
from consumers.base_consumer import BaseConsumer
from producers.person_producer import PersonProducer
from config.settings import CONSUMER_CONFIG

class HtmlConsumer(BaseConsumer):

    def __init__(self):
        super().__init__("HtmlConsumerSpark")
        self.producer = PersonProducer()

    def process_message(self):
        schema = ArrayType(StructType([
            StructField("file_path", StringType(), True),
            StructField("title", StringType(), True),
            StructField("content", StringType(), True)
        ]))

        extract_pages_spark_udf = udf(extract_pages_spark, schema)

        kafka_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", CONSUMER_CONFIG['bootstrap.servers']) \
            .option("subscribe", "html_topic") \
            .option("failOnDataLoss", "false") \
            .load()

        file_paths_df = kafka_df.selectExpr("CAST(value AS STRING) AS file_path")

        flat_df = file_paths_df.withColumn("page", explode(extract_pages_spark_udf("file_path")))

        final_df = flat_df.select(
            col("page.file_path"),
            col("page.title"),
            col("page.content")
        )

        query = final_df.writeStream \
            .option("checkpointLocation", "./spark_checkpoint/html_consumer/")\
            .foreachBatch(self.process_batch) \
            .outputMode("append") \
            .start()

        query.awaitTermination(timeout=10)

    def process_batch(self, batch_df, batch_id):
        for row in batch_df.collect():
            message = {
                "file_path": row.file_path,
                "title": row.title,
                "content": row.content
            }
            self.producer.produce_person(message)