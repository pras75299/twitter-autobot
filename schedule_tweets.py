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

def get_random_time():
    """Generate time with 10-minute intervals from current time between 8 AM and 10 PM."""
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute

    # Round up to next 10-minute interval
    next_minute = ((current_minute + 10) // 10) * 10

    # Adjust hour if minutes roll over
    hour = (current_hour + (next_minute // 60)) % 24
    minute = next_minute % 60

    # If time is before 8 AM, start at 8 AM
    if hour < 8:
        hour = 8
        minute = 0

    # If time is after 10 PM, schedule for next day at 8 AM
    if hour >= 22:
        hour = 8
        minute = 0

    return f"{hour:02d}:{minute:02d}"

def schedule_next_tweet(client, last_post_time):
    """Schedule the next tweet with at least a 10-minute interval."""
    while True:  # Loop to ensure at least 10-minute gap
        time_str = get_random_time()
        if last_post_time is None or (datetime.strptime(time_str, "%H:%M") - last_post_time) >= timedelta(minutes=10):
            break  # Valid time with at least 10-minute gap found
    schedule.every().day.at(time_str).do(post_random_tweet, client=client)
    logging.info(f"Scheduled tweet for {time_str}")
    return datetime.strptime(time_str, "%H:%M")

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

def run_bot():
    """Main bot running function."""
    client = authenticate()
    if client:
        logging.info("Starting Twitter Bot")
        last_post_time = None  # Initialize outside the loop
        for _ in range(15):
            last_post_time = schedule_next_tweet(client, last_post_time) 
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        logging.error("Failed to initialize Twitter client.")

if __name__ == "__main__":
    run_bot()