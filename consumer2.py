from confluent_kafka import Consumer
import os
from extract_data import extract_profile_info
import json

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

        print(f"Calling extract_profile_info...")
        profile = extract_profile_info(msg.value().decode('utf-8'))

        file_path = "output/data_profile.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            data.append(profile)
        else:
            data = [profile]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    consumer.close()


topic_name = "extract_data"
consume_and_process(topic_name)
