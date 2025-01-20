from confluent_kafka import Consumer
import json
import os
from process_data import process_file

kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'html_processor_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_config)

def consume_and_process(topic):
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        file_path = msg.value().decode('utf-8')
        print(f"Processing file: {file_path}")

        if os.path.exists(file_path):
            profile_data = process_file(file_path)
            output_path = file_path.replace(".xml", "_profile.json")

            with open(output_path, "w", encoding="utf-8") as output_file:
                json.dump(profile_data, output_file, indent=4)
            print(f"Saved profile data to: {output_path}")
        else:
            print(f"File not found: {file_path}")

        consumer.close()

topic_name = "test_topic"
consume_and_process(topic_name)
