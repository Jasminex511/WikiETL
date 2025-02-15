from confluent_kafka import Consumer
from config.settings import CONSUMER_CONFIG

class BaseConsumer:

    def __init__(self, topic):
        self.topic = topic
        self.consumer = Consumer(CONSUMER_CONFIG)
        self.consumer.subscribe([self.topic])

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
