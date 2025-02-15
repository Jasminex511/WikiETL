from processors.extract_data import extract_profile_info
import json
from consumers.base_consumer import BaseConsumer
from utils.database import collection

class PersonConsumer(BaseConsumer):

    def __init__(self):
        super().__init__(topic="person_topic")

    def process_message(self):
        print("PersonConsumer is processing message...")
        msg = self.consume_message()
        if msg:
            try:
                msg_str = msg.decode('utf-8')
                page_data = json.dumps(msg_str)
                print(f"Calling extract_profile_info...")
                profile = extract_profile_info(page_data)
                if profile:
                    collection.insert_one(json.loads(profile))
                    print("Profile inserted into MongoDB")
                else:
                    print("Failed to extract profile")
            except Exception as e:
                print(f"Error processing message: {e}")
        else:
            print("No new person message received.")