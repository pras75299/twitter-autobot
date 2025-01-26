from auth import authenticate
from generate_tweet import generate_tweet
import tweepy
import os

def post_tweet_v2(client, content):
    try:
        # Use v2 API's create_tweet method
        response = client.create_tweet(text=content)
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")

if __name__ == "__main__":
    # Authenticate with Twitter using v2 client
    client = tweepy.Client(
        bearer_token=os.getenv("BEARER_TOKEN"),
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )

    if client:
        topic = input("Enter a topic for the tweet: ")
        tweet_content = generate_tweet(topic)
        
        if tweet_content:
            print(f"Generated Tweet: {tweet_content}")
            confirm = input("Do you want to post this tweet? (y/n): ")
            if confirm.lower() == "y":
                post_tweet_v2(client, tweet_content)
            else:
                print("Tweet not posted.")
        else:
            print("Failed to generate a tweet.")

