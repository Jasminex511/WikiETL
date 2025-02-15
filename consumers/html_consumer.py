import os
import json
from processors.extract_pages import extract_person_pages
from consumers.base_consumer import BaseConsumer
from producers.person_producer import PersonProducer

class HtmlConsumer(BaseConsumer):

    def __init__(self):
        super().__init__(topic="html_topic")
        self.producer = PersonProducer()

    def process_message(self):
        msg = self.consumer.poll(1.0)
        if msg is None:
            return

        if msg.error():
            print(f"Consumer error: {msg.error()}")
            return

        raw_msg = msg.value()
        decoded_msg = raw_msg.decode('utf-8')
        print(f"Processing file: {decoded_msg}")
        if os.path.exists(decoded_msg):
            person_pages = extract_person_pages(decoded_msg)
            print(f"Extracted {len(person_pages)} pages.")
            for page in person_pages:
                self.producer.produce_person(page)
        else:
            print(f"File not found: {decoded_msg}")
