import time
import logging
import threading
from producers.html_producer import HtmlProducer
from consumers.html_consumer import HtmlConsumer
from consumers.person_consumer import PersonConsumer
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting all producer and consumer daemons...")

    try:
        html_consumer = HtmlConsumer()
        html_thread = threading.Thread(target=html_consumer.process_message, daemon=True)
        html_thread.start()

        person_consumer = PersonConsumer()
        person_thread = threading.Thread(target=person_consumer.process_message, daemon=True)
        person_thread.start()

        time.sleep(5)

        html_producer = HtmlProducer()
        html_producer.produce_html_files("sample_html")

        html_thread.join()
        person_thread.join()

    except Exception as e:
        logger.exception("Error in daemon")

    finally:
        logger.info("Stopping consumer daemons gracefully.")

if __name__ == "__main__":
    main()