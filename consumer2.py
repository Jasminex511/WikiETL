from confluent_kafka import Consumer
from extract_data import extract_profile_info
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'html_processor_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_config)

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["profile_database"]
collection = db["profiles"]

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

        collection.insert_one(json.loads(profile))
        print("Profile inserted into MongoDB")

    consumer.close()


topic_name = "extract_data"
consume_and_process(topic_name)
