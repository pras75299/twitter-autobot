from schedule_tweets import run_bot
import logging
import sys

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("tweet_bot.log")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

if __name__ == "__main__":
    try:
        logging.info("Starting autonomous Twitter bot...")
        # Run bot directly since we don't need threading anymore
        run_bot()
    except KeyboardInterrupt:
        logging.info("Twitter bot stopped by user.")
        print("Bot stopped by user.")
    except Exception as e:
        logging.error(f"Twitter bot crashed: {e}")
        print(f"Bot crashed: {e}")
    finally:
        handler.close()
        logging.shutdown()
        sys.exit(0)
