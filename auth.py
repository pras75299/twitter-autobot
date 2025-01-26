# auth.py
import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def authenticate():
    # Fetch credentials from .env
    bearer_token = os.getenv("BEARER_TOKEN")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # Authenticate using tweepy.Client (v2 API)
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    print("Authentication successful!")
    return client
