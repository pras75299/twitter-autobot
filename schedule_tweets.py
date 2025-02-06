import schedule
import time
import random
import logging
from generate_tweet import generate_tweet
from datetime import datetime, timedelta
from auth import authenticate
from pytz import timezone
IST = timezone('Asia/Kolkata')
DAILY_LIMIT = 15

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


def get_todays_tweet_count(client):
    """Get number of tweets posted today using Twitter API"""
    try:
        user_id = client.get_me().data.id
        now = datetime.now(IST)
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        response = client.get_users_tweets(
            id=user_id,
            start_time=start_time.isoformat(),
            max_results=100  # More than enough for 15-tweet limit
        )
        
        if response.data:
            return len(response.data)
        return 0
    except Exception as e:
        logging.error(f"Error getting tweet count: {e}")
        return 0  # Fail-safe to prevent blocking


def get_next_time(last_post_time):
    """Calculate next post time with minimum 10-minute gap within 8AM-10PM window"""
    now = datetime.now(IST)
    
    if last_post_time is None:
        # Start at next 8 AM if current time < 8 AM
        base_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if now < base_time:
            return base_time
        # Otherwise start with minimum gap
        return now + timedelta(minutes=10)
    
    # Calculate next time with random interval
    next_time = last_post_time + timedelta(minutes=random.randint(10, 60))
    
    # Clamp to 8AM-10PM window
    next_day = next_time + timedelta(days=1)
    earliest = next_time.replace(hour=8, minute=0, second=0, microsecond=0)
    latest = next_time.replace(hour=22, minute=0, second=0, microsecond=0)
    
    if next_time > latest:
        # If past 10PM, move to next day 8AM
        return earliest + timedelta(days=1)
    elif next_time < earliest:
        # If before 8AM, move to 8AM same day
        return earliest
    return next_time


def post_immediate_tweets(client):
    """Post 5 tweets with 2-minute gaps"""
    from time import sleep
    for _ in range(5):
        try:
            post_random_tweet(client)
            sleep(120)  # 2-minute gap
        except Exception as e:
            logging.error(f"Immediate posting failed: {e}")


def schedule_daily_tweets(client):
    """Schedule all daily tweets at once with proper spacing"""
    last_time = None
    scheduled_times = []
    
    # Generate all 15 times first
    for _ in range(15):
        next_time = get_next_time(last_time)
        scheduled_times.append(next_time)
        last_time = next_time

    # Schedule each time
    for st in scheduled_times:
        schedule.every().day.at(st.strftime("%H:%M")).do(post_random_tweet, client=client)
        logging.info(f"Scheduled tweet for {st.strftime('%Y-%m-%d %H:%M')}")

def post_random_tweet(client):
    """Generate and post a tweet about a random topic with limit check."""
    try:
        # Check daily limit first
        tweet_count = get_todays_tweet_count(client)
        if tweet_count >= DAILY_LIMIT:
            logging.warning(f"Daily limit reached ({tweet_count}/{DAILY_LIMIT}). Skipping tweet.")
            return

        topic = random.choice(TOPICS)
        logging.info(f"Generating tweet for topic: {topic}")
        tweet_content = generate_tweet(topic)

        if tweet_content:
            logging.info(f"Generated Tweet: {tweet_content}")
            response = client.create_tweet(text=tweet_content)
            logging.info(f"Tweet posted successfully. ID: {response.data['id']}")
            logging.info(f"Daily count: {tweet_count + 1}/{DAILY_LIMIT}")
        else:
            logging.error(f"Failed to generate tweet about {topic}")
    except Exception as e:
        logging.error(f"Error in post_random_tweet: {e}")

def post_immediate_tweets(client):
    """Post 5 tweets with 2-minute gaps and limit checks"""
    from time import sleep
    for i in range(5):
        tweet_count = get_todays_tweet_count(client)
        if tweet_count >= DAILY_LIMIT:
            logging.warning(f"Daily limit reached during immediate posting ({tweet_count}/{DAILY_LIMIT})")
            return
        
        post_random_tweet(client)
        if i < 4:  # No sleep after last tweet
            sleep(120)

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