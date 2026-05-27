import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
)

try:
    response = client.create_tweet(
        text="Testing X API integration from my AI bot 🚀"
    )
    print("SUCCESS:", response)

except Exception as e:
    print("ERROR:", e)