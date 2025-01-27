import schedule
import time
import random
import logging
from generate_tweet import generate_tweet
from datetime import datetime
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
    "Python Programming",
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
    "Tech Humor",
    "Humor on DSA",
    "Tip for DSA",
    "Humor on College Life / School Life",
    "Corporate Humor"
]

def get_random_time():
    """Generate random time between 8 AM and 10 PM."""
    hour = random.randint(8, 22)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def schedule_tweets(client):
    """Schedule 15 tweets throughout the day."""
    # Clear any existing jobs
    schedule.clear()
    
    # Create 15 randomly spaced tweets
    posted_times = set()
    for _ in range(15):
        while True:
            time_str = get_random_time()
            if time_str not in posted_times:
                posted_times.add(time_str)
                schedule.every().day.at(time_str).do(post_random_tweet, client=client)
                logging.info(f"Scheduled tweet for {time_str}")
                break

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
            return True
        else:
            logging.error(f"Failed to generate tweet about {topic}")
            return False
    except Exception as e:
        logging.error(f"Error in post_random_tweet: {e}")
        return False

def run_bot():
    """Main bot running function."""
    client = authenticate()
    if client:
        logging.info("Starting Twitter Bot")
        schedule_tweets(client)
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        logging.error("Failed to initialize Twitter client.")
