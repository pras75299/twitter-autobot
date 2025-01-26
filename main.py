from auth import authenticate
from generate_tweet import generate_tweet

def post_tweet(api, content):
    try:
        api.update_status(content)
        print("Tweet posted successfully!")
    except Exception as e:
        print(f"Error posting tweet: {e}")

if __name__ == "__main__":
    # Authenticate with Twitter
    api = authenticate()
    if api:
        topic = input("Enter a topic for the tweet: ")
        tweet_content = generate_tweet(topic)
        
        if tweet_content:
            print(f"Generated Tweet: {tweet_content}")
            confirm = input("Do you want to post this tweet? (yes/no): ")
            if confirm.lower() == "yes":
                post_tweet(api, tweet_content)
            else:
                print("Tweet not posted.")
        else:
            print("Failed to generate a tweet.")
