from schedule_tweets import run_bot
import logging
from flask import Flask
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("tweet_bot.log"),  # Log to local file
        logging.StreamHandler()               # Log to stdout (Render dashboard)
    ]
)

app = Flask(__name__)

@app.route("/")
def home():
    return "Twitter Autobot is running!"

if __name__ == "__main__":
    try:
        logging.info("Starting autonomous Twitter bot...")
        # Run bot in background thread
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        # Start Flask server
        app.run(host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        logging.info("Twitter bot stopped by user.")
        print("Bot stopped by user.")
    except Exception as e:
        logging.error(f"Twitter bot crashed: {e}")
        print(f"Bot crashed: {e}")
