# scheduler.py
import schedule
import time
from main import post_tweet, authenticate

def schedule_tweet(api, content, time_str):
    schedule.every().day.at(time_str).do(post_tweet, api=api, content=content)
    print(f"Scheduled tweet for {time_str}")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    api = authenticate()
    if api:
        content = input("Enter the tweet content: ")
        time_str = input("Enter the time to post (HH:MM): ")
        schedule_tweet(api, content, time_str)
