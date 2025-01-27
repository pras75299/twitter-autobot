from schedule_tweets import run_bot
import logging

# Configure logging
logging.basicConfig(
    filename="tweet_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    try:
        logging.info("Starting autonomous Twitter bot...")
        run_bot()
    except KeyboardInterrupt:
        logging.info("Twitter bot stopped by user.")
        print("Bot stopped by user.")
    except Exception as e:
        logging.error(f"Twitter bot crashed: {e}")
        print(f"Bot crashed: {e}")
