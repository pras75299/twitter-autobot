import schedule
import time
import random
import logging
from datetime import datetime, timedelta
from auth import authenticate
from generate_tweet import generate_tweet
from langgraph.graph import StateGraph
from langgraph.pylangchain import ToolNode
from langchain.tools import Tool

# Configure logging
logging.basicConfig(filename="tweet_bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TOPICS = [
    "AI and Machine Learning",
    "Python Programming",
    "Web Development",
    "Software Engineering Tips",
    "Tech Industry News",
    "Developer Productivity",
    "Programming Humor",
    "Blockchain",
    "Startup Culture"
]

# Function to select a random topic
def pick_topic():
    return random.choice(TOPICS)

# Function to determine whether to post a single tweet or thread
def decide_format():
    return random.choice(["single_tweet", "thread"])

# Function to generate tweets
def create_tweet(state):
    topic = pick_topic()
    tweet = generate_tweet(topic)
    return {"tweet": tweet}

# Define workflow graph
workflow = StateGraph()
workflow.add_node("pick_topic", ToolNode(Tool.from_function(pick_topic)))
workflow.add_node("decide_format", ToolNode(Tool.from_function(decide_format)))
workflow.add_node("create_tweet", ToolNode(Tool.from_function(create_tweet)))

workflow.add_edge("pick_topic", "decide_format")
workflow.add_edge("decide_format", "create_tweet")

graph = workflow.compile()

def post_tweet(client):
    """Run the graph to determine what to post and execute it."""
    result = graph.invoke({})
    tweet = result["create_tweet"]["tweet"]

    try:
        response = client.create_tweet(text=tweet)
        logging.info(f"Tweet posted successfully. ID: {response.data['id']}")
    except Exception as e:
        logging.error(f"Error posting tweet: {e}")

def schedule_tweets(client):
    """Schedule 15 tweets per day."""
    schedule.clear()
    for _ in range(15):
        schedule.every().hour.at(":00").do(post_tweet, client=client)
    logging.info("Scheduled tweets for the day.")

def run_bot():
    client = authenticate()
    if client:
        logging.info("Starting Twitter Bot with LangGraph workflow")
        schedule_tweets(client)
        while True:
            schedule.run_pending()
            time.sleep(60)
