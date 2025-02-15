import logging
import os

def setup_logging(log_level=logging.INFO, log_file="app.log"):

    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file_path = os.path.join("logs", log_file)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    return logger
