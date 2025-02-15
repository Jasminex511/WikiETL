PRODUCER_CONFIG = {
    'bootstrap.servers': 'localhost:9092'
}

CONSUMER_CONFIG  = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'html_processor_group',
    'auto.offset.reset': 'earliest'
}