from confluent_kafka import Consumer
import json
import os
from extract_pages import extract_person_pages

kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'html_processor_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_config)

def consume_and_process(topic, output_dir):
    consumer.subscribe([topic])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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
            person_pages = extract_person_pages(file_path)
            for page in person_pages:
                # TODO: send to consumer2.py, which calls keyword_generation.py
            output_filename = os.path.basename(file_path).replace(".xml", "_profile.json")
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "w", encoding="utf-8") as output_file:
            print(f"Saved profile data to: {output_path}")
        else:
            print(f"File not found: {file_path}")

    consumer.close()

topic_name = "parse_html"
output_directory = "output"
consume_and_process(topic_name, output_directory)
