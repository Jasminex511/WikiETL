from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col, from_json
from pydantic import ValidationError
import json
from consumers.base_consumer import BaseConsumer
from processors.extract_data import extract_profile_info
from utils.database import collection
from utils.format import person
from config.settings import CONSUMER_CONFIG

class PersonConsumer(BaseConsumer):

    def __init__(self):
        super().__init__("PersonConsumerSpark")

    def process_message(self):

        schema = StructType([
            StructField("file_path", StringType(), True),
            StructField("title", StringType(), True),
            StructField("content", StringType(), True)
        ])

        kafka_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", CONSUMER_CONFIG['bootstrap.servers']) \
            .option("subscribe", "person_topic") \
            .option("failOnDataLoss", "false") \
            .load()

        messages_df = kafka_df.selectExpr("CAST(value AS STRING) as message")

        structured_df = messages_df.withColumn("json_data", from_json(col("message"), schema))

        final_df = structured_df.select(
            col("json_data.file_path").alias("file_path"),
            col("json_data.title").alias("title"),
            col("json_data.content").alias("content")
        )

        query = final_df.writeStream \
            .foreachBatch(self.process_batch) \
            .outputMode("append") \
            .option("checkpointLocation", "./spark_checkpoint/person_consumer/")\
            .start()

        query.awaitTermination()

    def process_batch(self, batch_df, batch_id):
        for row in batch_df.collect():
            try:
                message = {
                    "file_path": row.file_path,
                    "title": row.title,
                    "content": row.content
                }

                profile_json = extract_profile_info(json.dumps(message))
                profile_data = json.loads(profile_json)

                validated_person = person(**profile_data)
                person_dict = validated_person.model_dump()

                collection.insert_one(person_dict)
                print(f"Profile inserted into MongoDB: {validated_person.name}")

            except ValidationError as e:
                print(f"Validation error: {e.json()}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
            except Exception as e:
                print(f"Error processing message: {str(e)}")
