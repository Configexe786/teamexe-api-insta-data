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
        return jsonify({"status": "error", "message": "Unauthorized!"}), 401

    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Username missing."}), 400

    headers = {"Content-Type": "application/json", "x-api-key": HASDATA_API_KEY}
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return jsonify({"status": "success", "dev": "@Configexe", "data": response.json()})
        return jsonify({"status": "error", "message": "Data fetch failed"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    # Improved UI with Bold Fonts and Telegram Button
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>TeamExe API</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background-color: #f4f4f9; padding-top: 50px; }
            .container { background: white; padding: 30px; border-radius: 15px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h1 { color: #333; margin-bottom: 20px; font-size: 24px; }
            .info { font-size: 18px; color: #444; margin: 10px 0; font-weight: 600; }
            .btn { 
                display: inline-block; margin-top: 20px; padding: 12px 25px; 
                background-color: #0088cc; color: white; text-decoration: none; 
                border-radius: 8px; font-weight: bold; transition: 0.3s;
            }
            .btn:hover { background-color: #006699; transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>TeamExe Secure IG Scraper API is Live!</h1>
            <div class="info">Developer: Teamexe</div>
            <div class="info">Telegram: @Configexe</div>
            <a href="https://t.me/configexe" class="btn">Contact Telegram</a>
        </div>
    </body>
    </html>
    '''

app = app
