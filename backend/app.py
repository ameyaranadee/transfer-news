import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

BEARER_TOKEN = os.getenv('X_API_BEARER')
FABRIZIO_USERNAME = "FabrizioRomano"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

def get_dummy_tweets():
    return [
        {
            "id": "1781234567890123456",
            "text": "Here we go! João Neves to Manchester United, agreement reached. 🔴 #MUFC",
            "created_at": "2024-05-25T17:03:02.000Z"
        },
        {
            "id": "1782345678901234567",
            "text": "Official: Kylian Mbappé joins Real Madrid on free transfer. Statement expected soon. ⚪️ #RealMadrid",
            "created_at": "2024-05-25T14:45:10.000Z"
        },
        {
            "id": "1783456789012345678",
            "text": "Deal confirmed. Mason Greenwood leaves Manchester United, signs for Juventus. ✍️ #Juventus",
            "created_at": "2024-05-25T12:01:28.000Z"
        },
        {
            "id": "1784567890123456789",
            "text": "Loan deal: Marc Cucurella joins Sevilla from Chelsea until June 2025. #CFC #SevillaFC",
            "created_at": "2024-05-25T10:21:00.000Z"
        }
    ]

def get_user_id():
    url = f"https://api.twitter.com/2/users/by/username/{FABRIZIO_USERNAME}"
    response = requests.get(url, headers=headers)
    print('Response status code:', response.status_code)
    return response.json().get("data", {}).get("id")

def get_tweets(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": 100,
        "tweet.fields": "created_at"
    }
    response = requests.get(url, headers=headers, params=params)
    print('Response status code:', response.status_code)
    return response.json().get("data", [])

@app.route("/api/tweets")
def tweets():
    user_id = get_user_id()
    print('user_id:', user_id)
    if not user_id:
        return jsonify({"error": "User not found"}), 500

    try:
        # tweets = get_dummy_tweets()
        tweets = get_tweets(user_id)
        return jsonify({"tweets": tweets})
    except Exception as e:
        return jsonify({ "error": str(e), "tweets": [] }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)