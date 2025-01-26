import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def authenticate():
    # Fetch credentials from .env
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # Authenticate using OAuth 1.0a for posting tweets
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication successful!")
        return api
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
