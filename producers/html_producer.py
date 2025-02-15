import os
from producers.base_producer import BaseProducer

class HtmlProducer(BaseProducer):

    def __init__(self):
        super().__init__(topic="html_topic")

    def produce_html_files(self, directory):
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory.")
            return

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            if os.path.isfile(file_path) and '.xml' in filename:
                print(f"Producing: {file_path}")
                self.send_message(file_path)
