import json
from producers.base_producer import BaseProducer

class PersonProducer(BaseProducer):

    def __init__(self):
        super().__init__(topic="person_topic")

    def produce_person(self, person):
        self.send_message(person)