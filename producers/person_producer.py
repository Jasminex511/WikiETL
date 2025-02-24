import json
from producers.base_producer import BaseProducer

class PersonProducer(BaseProducer):

    def __init__(self):
        super().__init__(topic="person_topic")

    def produce_person(self, person):
        self.send_message(person)

    # def produce_person_spark(self, batch_df, batch_id):
    #     batch_df.collect()
    #     for row in batch_df.collect():
    #         message = {
    #             "file_path": row.file_path,
    #             "page_title": row.page_title,
    #             "content": row.content
    #         }
    #         self.produce_person(json.dumps(message))
    #         print(f"Sent processed page: {row.page_title}")