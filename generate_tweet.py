import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_tweet(topic):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Write a short, engaging tweet about {topic}."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.7
        )
        tweet = response['choices'][0]['message']['content'].strip()
        return tweet
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return None
