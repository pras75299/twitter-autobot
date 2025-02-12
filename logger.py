from langsmith import trace
import logging

# Configure logging
logging.basicConfig(filename="logs/bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@trace
def log_success(message):
    logging.info(message)

@trace
def log_error(error):
    logging.error(error)
