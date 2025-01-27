from schedule_tweets import run_bot
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("tweet_bot.log")
    ]
)

if __name__ == "__main__":
    try:
        logging.info("Starting autonomous Twitter bot...")
        # Run bot directly since we don't need threading anymore
        run_bot()
    except KeyboardInterrupt:
        logging.info("Twitter bot stopped by user.")
        logging.error(f"Twitter bot crashed: {e}")
        print(f"Bot crashed: {e}")
    finally:
        handler.close()
        logging.shutdown()
        sys.exit(0)
