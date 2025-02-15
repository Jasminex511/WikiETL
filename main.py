import time
import signal
import logging
from producers.html_producer import HtmlProducer
from producers.person_producer import PersonProducer
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


def main():
    person_consumer = PersonConsumer()
    html_consumer = HtmlConsumer()
    html_producer = HtmlProducer()

    logger.info("Starting all producer and consumer daemons...")

    try:
        html_producer.produce_html_files("sample_html")
        while running:
            html_consumer.process_message()
            person_consumer.process_message()
            time.sleep(1)

    except Exception as e:
        logger.exception("Error in daemon")

    finally:
        logger.info("Stopping consumer daemons gracefully.")
        html_consumer.close()
        person_consumer.close()


if __name__ == "__main__":
    main()