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
        return jsonify({"status": "error", "message": "Access Denied!"}), 401

    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Target missing."}), 400

    headers = {"Content-Type": "application/json", "x-api-key": HASDATA_API_KEY}
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return jsonify({"status": "success", "dev": "@Configexe", "data": response.json()})
        return jsonify({"status": "error", "message": "Extraction failed"}), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    # Matrix Hacker Theme Animation
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TeamExe Hacker API</title>
        <style>
            body { margin: 0; padding: 0; background: black; overflow: hidden; font-family: 'Courier New', Courier, monospace; }
            canvas { display: block; }
            .content {
                position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.85); padding: 40px; border: 2px solid #0f0;
                border-radius: 10px; text-align: center; color: #0f0;
                box-shadow: 0 0 20px #0f0; z-index: 10; width: 80%; max-width: 500px;
            }
            h1 { font-size: 22px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px #0f0; }
            .info { font-size: 18px; margin: 15px 0; font-weight: bold; }
            .btn {
                display: inline-block; margin-top: 25px; padding: 12px 30px;
                border: 2px solid #0f0; color: #0f0; text-decoration: none;
                font-weight: bold; text-transform: uppercase; transition: 0.4s;
                background: transparent; cursor: pointer;
            }
            .btn:hover { background: #0f0; color: #000; box-shadow: 0 0 30px #0f0; }
        </style>
    </head>
    <body>
        <canvas id="matrix"></canvas>
        <div class="content">
            <h1>TeamExe Secure IG Scraper API</h1>
            <div class="info">SYSTEM STATUS: LIVE</div>
            <div class="info">Developer: Teamexe</div>
            <div class="info">Telegram: @Configexe</div>
            <a href="https://t.me/configexe" class="btn">Contact Telegram</a>
        </div>

        <script>
            const canvas = document.getElementById('matrix');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()*&^%";
            const fontSize = 16;
            const columns = canvas.width / fontSize;
            const drops = Array(Math.floor(columns)).fill(1);

            function draw() {
                ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#0f0";
                ctx.font = fontSize + "px monospace";

                for (let i = 0; i < drops.length; i++) {
                    const text = characters.charAt(Math.floor(Math.random() * characters.length));
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }
                    drops[i]++;
                }
            }
            setInterval(draw, 33);
        </script>
    </body>
    </html>
    '''

app = app
    
