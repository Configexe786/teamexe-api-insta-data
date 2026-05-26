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
    
    # Unauthorized Error (401)
    if user_key != MY_OWN_API_SECURE_KEY:
        return jsonify({
            "status": "error", 
            "status_code": 401,
            "message": "Access Denied! Invalid API Key."
        }), 401

    username = request.args.get('username')
    # Bad Request Error (400)
    if not username:
        return jsonify({
            "status": "error", 
            "status_code": 400,
            "message": "Target username missing."
        }), 400

    headers = {"Content-Type": "application/json", "x-api-key": HASDATA_API_KEY}
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        
        # Success (200)
        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "status_code": 200,
                "dev": "@Configexe",
                "data": response.json()
            }), 200
        
        # Data Fetching / Private Account Error (404/500)
        else:
            return jsonify({
                "status": "error", 
                "status_code": response.status_code,
                "message": "Extraction failed. Target account might be private or doesn't exist."
            }), response.status_code

    except Exception as e:
        # Internal Server Error (500)
        return jsonify({
            "status": "error", 
            "status_code": 500,
            "message": str(e)
        }), 500

@app.route('/')
def home():
    # Matrix Sharp UI remains the same
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
                background: rgba(0, 15, 0, 0.95); padding: 25px; border: 2px solid #0f0;
                border-radius: 8px; text-align: center; color: #0f0;
                box-shadow: 0 0 20px #0f0; z-index: 10; width: 85%; max-width: 380px;
            }
            h1 { font-family: 'Press Start 2P', cursive; font-size: 13px; line-height: 1.8; margin-bottom: 20px; color: #0f0; text-shadow: 2px 2px #000; }
            .info { font-size: 17px; margin: 12px 0; border-bottom: 1px solid #040; padding-bottom: 8px; letter-spacing: 1px; }
            .note-box { margin: 20px 0; padding: 10px; border: 1px double #f00; background: rgba(50, 0, 0, 0.3); }
            .note-text { font-size: 14px; color: #ff3333; font-family: 'Share Tech Mono', monospace; font-weight: bold; line-height: 1.4; text-transform: uppercase; }
            .btn { display: inline-block; margin-top: 10px; padding: 12px 24px; border: 2px solid #0f0; color: #0f0; text-decoration: none; font-weight: bold; font-family: 'Press Start 2P', cursive; font-size: 9px; transition: 0.3s; background: transparent; cursor: pointer; }
            .btn:hover { background: #0f0; color: #000; box-shadow: 0 0 25px #0f0; }
        </style>
    </head>
    <body>
        <canvas id="matrix"></canvas>
        <div class="content">
            <h1>TEAMEXE SECURE IG SCRAPER API</h1>
            <div class="info">STATUS: ONLINE</div>
            <div class="info">DEV: TEAMEXE</div>
            <div class="info">TG: @CONFIGEXE</div>
            <div class="note-box">
                <span class="note-text">ACCESS DENIED? CONTACT DEVELOPER ON TELEGRAM TO PURCHASE A PRIVATE API KEY.</span>
            </div>
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
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) { drops[i] = 0; }
                    drops[i]++;
                }
            }
            setInterval(draw, 40);
        </script>
    </body>
    </html>
    '''

app = app
                                
