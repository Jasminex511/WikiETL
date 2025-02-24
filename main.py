import time
import signal
import logging
import threading
from producers.html_producer import HtmlProducer
from consumers.html_consumer import HtmlConsumer
from consumers.person_consumer import PersonConsumer
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

running = True

def shutdown_handler(signum, frame):
    global running
    logger.info("Shutdown signal received.")
    running = False

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


def run_html_consumer(html_consumer):
    while running:
        html_consumer.process_message()
        time.sleep(1)

def run_person_consumer(person_consumer):
    while running:
        person_consumer.process_message()
        time.sleep(1)

def main():
    person_consumer = PersonConsumer()
    html_consumer = HtmlConsumer()
    html_producer = HtmlProducer()

    logger.info("Starting all producer and consumer daemons...")

    try:
        html_producer.produce_html_files("sample_html")

        # Running both consumers in separate threads
        html_thread = threading.Thread(target=run_html_consumer, args=(html_consumer,))
        person_thread = threading.Thread(target=run_person_consumer, args=(person_consumer,))

        html_thread.start()
        person_thread.start()

        # Main thread waits for the threads to complete
        html_thread.join()  # Will block until the html_consumer is finished
        person_thread.join()  # Will block until the person_consumer is finished

    except Exception as e:
        logger.exception("Error in daemon")

    finally:
        logger.info("Stopping consumer daemons gracefully.")
        html_consumer.close()
        person_consumer.close()


if __name__ == "__main__":
    main()
