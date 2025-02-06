from confluent_kafka import Producer
import json

kafka_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(kafka_config)

def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_pages(content, topic):
    message = json.dumps(content)
    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.flush()
