# logger.py
import logging

# Configure logging
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_success(message):
    logging.info(message)

def log_error(error):
    logging.error(error)
