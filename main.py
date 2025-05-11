import time
import random
import logging
from logger import setup_logger
from telegram_notifier import send_telegram_message
from parser import check_book_availability

setup_logger()

while True:
    logging.info("Starting new check")
    availability = check_book_availability()

    if availability:
        send_telegram_message(f"Availability: {availability}")

    delay = random.randint(900, 1500)
    logging.info(f"Sleeping for {delay // 60} minutes")
    time.sleep(delay)
