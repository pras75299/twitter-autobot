# main.py
from auth import authenticate

def post_tweet(client, content):
    try:
        # Use v2 create_tweet method
        response = client.create_tweet(text=content)
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

if __name__ == "__main__":
    client = authenticate()
    if client:
        content = input("Enter your tweet: ")
        post_tweet(client, content)
