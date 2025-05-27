import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify
load_dotenv()

app = Flask(__name__)

BEARER_TOKEN = os.getenv('X_API_BEARER')
FABRIZIO_USERNAME = "FabrizioRomano"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

def get_user_id():
    url = f"https://api.twitter.com/2/users/by/username/{FABRIZIO_USERNAME}"
    response = requests.get(url, headers=headers)
    print('Response status code:', response.status_code)
    return response.json().get("data", {}).get("id")

@app.route("/api/tweets")
def tweets():
    user_id = get_user_id()
    print('user_id:', user_id)
    return jsonify({"user_id": user_id})

if __name__ == "__main__":
    app.run(debug=True)