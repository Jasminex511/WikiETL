import os
from confluent_kafka import Producer

kafka_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(kafka_config)

def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_html_files(directory, topic):
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and '.xml' in filename:
            print(f"Producing: {file_path}")
            producer.produce(topic, file_path, callback=delivery_report)

    producer.flush()


directory_path = "sample_html"
topic_name = "parse_html"
produce_html_files(directory_path, topic_name)
