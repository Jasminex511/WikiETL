from pyspark.sql import SparkSession

class BaseConsumer:

    def __init__(self, appname):
        self.spark = SparkSession.builder \
            .appName(appname) \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
            .getOrCreate()

    def consume_message(self):
        msg = self.consumer.poll(1.0)
        if msg is None:
            return None
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            return None
        return msg.value()

    def close(self):
        if self.consumer:
            print("Closing Kafka consumer...")
            self.consumer.close()
            self.consumer = None
            print("Kafka consumer closed successfully.")
