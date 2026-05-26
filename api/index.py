from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# HasData Config
HASDATA_API_KEY = "fe8ccbd8-88d3-44dd-bf51-390a180d1ed0"
HASDATA_URL = "https://api.hasdata.com/scrape/instagram/profile"

# SECURITY KEY
MY_OWN_API_SECURE_KEY = "TEAMEXE786" 

# HTML Template for Matrix Theme
MATRIX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teamexe Insta API - Data</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 20px; background: black; font-family: 'Share Tech Mono', monospace; color: #0f0; overflow-x: hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.5; }
        .data-container {
            background: rgba(0, 20, 0, 0.9); border: 2px solid #0f0;
            padding: 20px; border-radius: 8px; box-shadow: 0 0 20px #0f0;
            max-width: 600px; margin: 50px auto; overflow-x: auto;
        }
        h2 { text-align: center; border-bottom: 2px solid #0f0; padding-bottom: 10px; margin-top: 0; }
        pre { white-space: pre-wrap; word-wrap: break-word; font-size: 14px; color: #0f0; }
        .status-box { text-align: center; margin-bottom: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="data-container">
        <h2>EXTRACTED DATA</h2>
        <div class="status-box">STATUS: SUCCESS | CODE: 200</div>
        <pre>{{ json_data | safe }}</pre>
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

@app.route('/ig-extract')
def extract_instagram():
    user_key = request.args.get('key')
    if user_key != MY_OWN_API_SECURE_KEY:
        return jsonify({"status": "error", "status_code": 401, "message": "Access Denied!"}), 401

    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "status_code": 400, "message": "Username missing."}), 400

    headers = {"Content-Type": "application/json", "x-api-key": HASDATA_API_KEY}
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            full_data = response.json()
            # Filtering specific fields
            filtered_data = {
                "status": "success",
                "status_code": 200,
                "dev": "@Configexe",
                "data": {
                    "biography": full_data.get("biography"),
                    "fbid": full_data.get("fbid"),
                    "followersCount": full_data.get("followersCount"),
                    "followsCount": full_data.get("followsCount"),
                    "fullName": full_data.get("fullName"),
                    "highlightsCount": full_data.get("highlightsCount"),
                    "id": full_data.get("id"),
                    "igtvVideoCount": full_data.get("igtvVideoCount"),
                    "isProfessionalAccount": full_data.get("isProfessionalAccount")
                }
            }
            # Beautifying JSON with indentation
            pretty_json = json.dumps(filtered_data, indent=2)
            return render_template_string(MATRIX_HTML, json_data=pretty_json)
        
        else:
            return jsonify({"status": "error", "status_code": response.status_code, "message": "Failed."}), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)}), 500

@app.route('/')
def home():
    # Home UI from previous turn
    return render_template_string(MATRIX_HTML, json_data='''
    {
      "api": "Teamexe Insta API",
      "status": "ONLINE",
      "developer": "@Configexe",
      "note": "CONTACT TELEGRAM FOR API KEY"
    }
    ''')

app = app
        
