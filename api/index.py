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
    # Matrix Sharp UI with centered compact box
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TeamExe Hacker API</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; background: black; overflow: hidden; font-family: 'Share Tech Mono', monospace; }
            canvas { display: block; position: fixed; top: 0; left: 0; z-index: 1; }
            .content {
                position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: rgba(0, 20, 0, 0.9); padding: 25px; border: 1.5px solid #0f0;
                border-radius: 5px; text-align: center; color: #0f0;
                box-shadow: 0 0 15px #0f0; z-index: 10; width: 85%; max-width: 380px;
            }
            h1 { 
                font-family: 'Press Start 2P', cursive; font-size: 14px; 
                line-height: 1.6; margin-bottom: 20px; color: #0f0; 
                text-shadow: 2px 2px #003300; 
            }
            .info { font-size: 16px; margin: 10px 0; border-bottom: 1px dashed #0f0; padding-bottom: 5px; }
            .btn {
                display: inline-block; margin-top: 20px; padding: 10px 20px;
                border: 1px solid #0f0; color: #0f0; text-decoration: none;
                font-weight: bold; font-family: 'Press Start 2P', cursive; font-size: 10px;
                transition: 0.3s; background: transparent; cursor: pointer;
            }
            .btn:hover { background: #0f0; color: #000; box-shadow: 0 0 20px #0f0; }
        </style>
    </head>
    <body>
        <canvas id="matrix"></canvas>
        <div class="content">
            <h1>TEAMEXE SECURE IG SCRAPER API</h1>
            <div class="info">STATUS: ONLINE</div>
            <div class="info">DEV: TEAMEXE</div>
            <div class="info">TG: @CONFIGEXE</div>
            <a href="https://t.me/configexe" class="btn">CONTACT TELEGRAM</a>
        </div>

        <script>
            const canvas = document.getElementById('matrix');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const characters = "01";
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
            setInterval(draw, 40);
        </script>
    </body>
    </html>
    '''

app = app
    
