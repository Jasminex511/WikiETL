from confluent_kafka import Producer

kafka_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(kafka_config)

def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_html_files(directory, topic):
    producer.produce(topic, directory, callback=delivery_report)
    print(f"Produced: {directory}")

    producer.flush()

directory_path = "data.xml"
topic_name = "test_topic"
produce_html_files(directory_path, topic_name)
