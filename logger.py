import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File output
    file_handler = logging.FileHandler("parser.log", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Consol output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
