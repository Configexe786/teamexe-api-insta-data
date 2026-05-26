from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# HasData Config
HASDATA_API_KEY = "fe8ccbd8-88d3-44dd-bf51-390a180d1ed0"
HASDATA_URL = "https://api.hasdata.com/scrape/instagram/profile"

# SECURITY KEY
MY_OWN_API_SECURE_KEY = "TEAMEXE786" 

@app.route('/ig-extract')
def extract_instagram():
    user_key = request.args.get('key')
    if user_key != MY_OWN_API_SECURE_KEY:
        return jsonify({"status": "error", "message": "Unauthorized! Please provide valid TeamExe API Key."}), 401

    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Username parameter is missing."}), 400

    headers = {
        "Content-Type": "application/json",
        "x-api-key": HASDATA_API_KEY
    }
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "dev": "@Configexe",
                "data": response.json()
            })
        else:
            return jsonify({"status": "error", "message": f"HasData Error: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    # Home page design update
    return '''
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>TeamExe Secure IG Scraper API is Live!</h1>
        <p style="font-weight: 100; color: #555; margin-top: -10px;">Developer: Teamexe</p>
        <p style="font-weight: 100; color: #555; margin-top: -10px;">Telegram: @Configexe</p>
    </div>
    '''

app = app
            
