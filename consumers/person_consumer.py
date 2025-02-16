from utils.format import person
from pydantic import ValidationError
import json
from processors.extract_data import extract_profile_info
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
                print("Calling extract_profile_info for message...")
                profile_json = extract_profile_info(msg_str)
                
                profile_data = json.loads(profile_json)
                validated_person = person(**profile_data)
                
                person_dict = validated_person.model_dump()
                
                collection.insert_one(person_dict)
                print(f"Profile inserted into MongoDB: {validated_person.name}")
                
            except ValidationError as e:
                print(f"Validation error: {e.json()}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
            except Exception as e:
                print(f"Error processing message: {str(e)}")
        else:
            print("No new person message received.")