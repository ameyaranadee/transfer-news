import os
import re
import json
import time
import requests
import instructor
from openai import OpenAI
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify
from models import db, Transfer
from schemas import Transfer

load_dotenv()

BEARER_TOKEN = os.getenv('X_API_BEARER')
FABRIZIO_USERNAME = "FabrizioRomano"
BASE_URL = "https://api.twitter.com/2"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transfers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

openai_client = instructor.patch(OpenAI(api_key=OPENAI_API_KEY))

# Cache config
tweet_cache = []
last_fetched = 0
FETCH_INTERVAL = 60 * 15  # 15 minutes to comply with free-tier rate limit

def get_dummy_tweets():
    with open("backend/dummy_tweets.json", "r") as file:
        dummy_tweets = json.loads(file.read())
    return dummy_tweets["tweets"]

def get_user_id():
    url = f"{BASE_URL}/users/by/username/{FABRIZIO_USERNAME}"
    response = requests.get(url, headers=headers)
    print('Response status code:', response.status_code)
    return response.json().get("data", {}).get("id")


def get_tweets(user_id):
    url = f"{BASE_URL}/users/{user_id}/tweets"
    params = {
        "max_results": 100,
        "tweet.fields": "created_at"
    }
    response = requests.get(url, headers=headers, params=params)
    print('Response status code:', response.status_code)
    return response.json().get("data", [])

def extract_transfer_from_tweet(tweet) -> Transfer:
    """
    Given a tweet dict with 'id' and 'text', extract structured transfer info.
    """
    return openai_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Transfer,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts football transfer information from tweets. "
                    "Extract as many fields as you can from the tweet text. "
                    "If a field is not available, use null. "
                    "Today's date is "
                    f"{datetime.now().date()}."
                )
            },
            {
                "role": "user",
                "content": (
                    "Given this tweet, extract a Python object with the fields: "
                    "transfer_id (tweet_id), status (one of: 'official', 'rumor', 'loan', or null), "
                    "player_name, from_club, to_club, transfer_amount, position. "
                    "Do NOT extract player_face_url or club logo URLs. "
                    "Do NOT extract transfer_time; it will be set from the tweet's created_at.\n\n"
                    f"tweet_id: {tweet['id']}\nTweet: {tweet['text']}"
                )
            }
        ],
        temperature=0,
    )

@app.route("/api/tweets")
def tweets():
    global tweet_cache, last_fetched
    now = time.time()
    if now - last_fetched > FETCH_INTERVAL:
        try:
            # user_id = get_user_id()
            # if not user_id:
            #     raise ValueError("Failed to fetch user ID")
            
            # raw_tweets = get_recent_tweets(user_id)
            raw_tweets = get_dummy_tweets()
            for tweet in raw_tweets:
                parsed = extract_transfer_from_tweet(tweet)
                if parsed and parsed.player_name:
                    transfer_time = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00")).date()
                    db_transfer = Transfer(
                        **parsed.dict(),
                        transfer_time=transfer_time,
                        player_face_url=None,               # will be filled later by another process
                        from_club_logo_url=None,            # same
                        to_club_logo_url=None               # same
                    )
                    if not Transfer.query.filter_by(transfer_id=db_transfer.transfer_id).first():
                        db.session.add(db_transfer)
            db.session.commit()
            tweet_cache = raw_tweets
            last_fetched = now
        except Exception as e:
            db.session.rollback()
            print(f"[WARN] Failed to update tweets: {e}")

    # Return all transfers (as dicts) for the frontend
    all_transfers = Transfer.query.order_by(Transfer.transfer_time.desc()).all()
    return jsonify([t.as_dict() for t in all_transfers])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5050)