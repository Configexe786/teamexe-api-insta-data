from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# HasData Config (Aapki di hui Key aur URL)
HASDATA_API_KEY = "fe8ccbd8-88d3-44dd-bf51-390a180d1ed0"
HASDATA_URL = "https://api.hasdata.com/scrape/instagram/profile"

# SECURITY: Ye aapki apni key hai. Isse aapka API secure rahega.
# Ise aap badal bhi sakte hain.
MY_OWN_API_SECURE_KEY = "TEAMEXE786" 

@app.route('/ig-extract')
def extract_instagram():
    # Step 1: Security Check (Key verification)
    user_key = request.args.get('key')
    if user_key != MY_OWN_API_SECURE_KEY:
        return jsonify({"status": "error", "message": "Unauthorized! Please provide valid TeamExe API Key."}), 401

    # Step 2: Username Check
    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Username parameter is missing."}), 400

    # Step 3: HasData API Request (Exact as per your cURL)
    headers = {
        "Content-Type": "application/json",
        "x-api-key": HASDATA_API_KEY
    }
    # HasData 'handle' parameter use karta hai
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
            return jsonify({
                "status": "error", 
                "message": f"HasData Server returned error {response.status_code}"
            }), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "<h1>TeamExe Secure IG Scraper API is Live!</h1>"

app = app
      
