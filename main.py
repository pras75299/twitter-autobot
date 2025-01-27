from schedule_tweets import run_bot
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("tweet_bot.log"),  # Log to local file
        logging.StreamHandler()               # Log to stdout (Render dashboard)
    ]
)
logging.getLogger().setLevel(logging.DEBUG)

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
