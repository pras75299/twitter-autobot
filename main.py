import logging
import sys
import argparse
import schedule
import time
from datetime import datetime, timedelta
from schedule_tweets import schedule_daily_tweets, post_immediate_tweets
from auth import authenticate

# Configure logging to log both to file and stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("tweet_bot.log"),  # Log to file
        logging.StreamHandler(sys.stdout)  # Log to console
    ]
)

def main(mode):
    """Main function to start the Twitter bot in either scheduled or immediate mode."""
    logging.info(f"Starting Twitter bot in {mode} mode...")

    # Authenticate Twitter client
    client = authenticate()
    if not client:
        logging.error("Failed to initialize Twitter client.")
        sys.exit(1)

    if mode == "scheduled":
        # Schedule tweets (max 15 per day at different times)
        logging.info("Scheduling tweets for the day...")
        schedule_daily_tweets(client)

        # Keep running to ensure all scheduled tweets are posted
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for pending jobs

    elif mode == "immediate":
        # Post 5 tweets immediately with a 5-minute gap
        logging.info("Posting 5 tweets immediately with 5-minute gaps...")
        post_immediate_tweets(client)

    else:
        logging.error("Invalid mode! Use 'scheduled' or 'immediate'.")
        sys.exit(1)

if __name__ == "__main__":
    # Accept mode as a command-line argument
    parser = argparse.ArgumentParser(description="Run Twitter bot in scheduled or immediate mode.")
    parser.add_argument("mode", choices=["scheduled", "immediate"], help="Choose mode: 'scheduled' or 'immediate'")
    args = parser.parse_args()

    try:
        main(args.mode)
    except KeyboardInterrupt:
        logging.info("Twitter bot stopped by user.")
    except Exception as e:
        logging.error(f"Twitter bot crashed: {e}")
    finally:
        logging.shutdown()
        sys.exit(0)
