from confluent_kafka import Producer
from config.settings import PRODUCER_CONFIG
from utils.kafka_helper import delivery_report
import json

class BaseProducer:

    def __init__(self, topic):
        self.topic = topic
        self.producer = Producer(PRODUCER_CONFIG)

    def send_message(self, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            self.producer.produce(self.topic, value=message.encode('utf-8'))
            self.producer.flush()
            print(f"Message delivered to {self.topic}")
        except Exception as e:
            print(f"Error producing message: {str(e)}")