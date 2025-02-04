import schedule
import time
import random
import logging
from generate_tweet import generate_tweet
from datetime import datetime, timedelta
from auth import authenticate

# Configure logging
logging.basicConfig(
    filename="tweet_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Topics to rotate through
TOPICS = [
    "AI and Machine Learning",
    "Tech Humor",
    "Humor on DSA",
    "Tip for DSA",
    "Humor on College",
    "Humor on Python Programming / Python Programming",
    "Web Development",
    "Software Engineering Tips",
    "Tech Industry News",
    "Coding Best Practices",
    "Developer Productivity",
    "Programming Humor",
    "Tech Career Advice",
    "Mobile Development",
    "Blockchain",
    "Cloud Computing",
    "DevOps",
]

def get_next_time(last_post_time):
    """Calculate next post time with minimum 10-minute gap within 8AM-10PM window"""
    if last_post_time is None:
        # Start at 8 AM today
        base_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        if datetime.now() > base_time:
            # If current time is past 8AM, start immediately with minimum gap
            return datetime.now() + timedelta(minutes=10)
        return base_time
    else:
        # Add random interval between 10-60 minutes
        return last_post_time + timedelta(minutes=random.randint(10, 60))

    # Ensure posts stay within 8AM-10PM window
    next_time = max(next_time, next_time.replace(hour=8, minute=0, second=0))
    next_time = min(next_time, next_time.replace(hour=22, minute=0, second=0))
    return next_time

def schedule_daily_tweets(client):
    """Schedule all daily tweets at once with proper spacing"""
    last_time = None
    for _ in range(15):
        next_time = get_next_time(last_time)
        schedule.every().day.at(next_time.strftime("%H:%M")).do(post_random_tweet, client=client)
        logging.info(f"Scheduled tweet for {next_time.strftime('%H:%M')}")
        last_time = next_time

def post_random_tweet(client):
    """Generate and post a tweet about a random topic."""
    try:
        topic = random.choice(TOPICS)
        logging.info(f"Generating tweet for topic: {topic}")
        tweet_content = generate_tweet(topic)

        if tweet_content:
            logging.info(f"Generated Tweet: {tweet_content}")
            response = client.create_tweet(text=tweet_content)
            logging.info(f"Tweet posted successfully. ID: {response.data['id']}")
        else:
            logging.error(f"Failed to generate tweet about {topic}")
    except Exception as e:
        logging.error(f"Error in post_random_tweet: {e}")

def post_now(client):
    """Immediate posting function"""
    try:
        topic = random.choice(TOPICS)
        tweet_content = generate_tweet(topic)
        if tweet_content:
            client.create_tweet(text=tweet_content)
            logging.info(f"Immediate tweet posted: {tweet_content}")
    except Exception as e:
        logging.error(f"Immediate post error: {e}")

def run_bot():
    """Main bot running function"""
    client = authenticate()
    if client:
        logging.info("Starting Twitter Bot")
        schedule_daily_tweets(client)
        
        # Keep running until all scheduled jobs are done
        start_time = datetime.now()
        while datetime.now() < start_time + timedelta(hours=14):  # Max 14h runtime
            schedule.run_pending()
            time.sleep(60)
    else:
        logging.error("Failed to initialize Twitter client.")

if __name__ == "__main__":
    run_bot()