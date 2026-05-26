from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# HasData Config
HASDATA_API_KEY = "fe8ccbd8-88d3-44dd-bf51-390a180d1ed0"
HASDATA_URL = "https://api.hasdata.com/scrape/instagram/profile"

# SECURITY KEY
MY_OWN_API_SECURE_KEY = "TEAMEXE786" 

# Base Matrix HTML Template
def get_matrix_template(title, heading, content, is_error=False):
    border_color = "#f00" if is_error else "#0f0"
    text_color = "#ff3333" if is_error else "#0f0"
    shadow_color = "#f00" if is_error else "#0f0"
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <style>
            body {{ margin: 0; padding: 20px; background: black; font-family: 'Share Tech Mono', monospace; color: {text_color}; overflow: hidden; }}
            canvas {{ position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.4; }}
            .container {{
                background: rgba(0, 5, 0, 0.95); border: 2px solid {border_color};
                padding: 25px; border-radius: 8px; box-shadow: 0 0 20px {shadow_color};
                max-width: 500px; margin: 80px auto; text-align: center; position: relative;
            {{
            h2 {{ border-bottom: 1px solid {border_color}; padding-bottom: 10px; text-transform: uppercase; }}
            .message {{ font-size: 16px; margin: 20px 0; line-height: 1.6; }}
            .btn {{
                display: inline-block; padding: 10px 20px; border: 1px solid {border_color};
                color: {text_color}; text-decoration: none; font-weight: bold; transition: 0.3s;
            }}
            .btn:hover {{ background: {border_color}; color: #000; }}
            pre {{ text-align: left; background: rgba(20, 0, 0, 0.5); padding: 15px; border-radius: 5px; color: #ff5555; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <canvas id="matrix"></canvas>
        <div class="container">
            <h2>{heading}</h2>
            <div class="message">{content}</div>
            <a href="https://t.me/configexe" class="btn">CONTACT SUPPORT</a>
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
            function draw() {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "{border_color}";
                ctx.font = fontSize + "px monospace";
                for (let i = 0; i < drops.length; i++) {{
                    const text = characters.charAt(Math.floor(Math.random() * characters.length));
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {{ drops[i] = 0; }}
                    drops[i]++;
                }}
            }}
            setInterval(draw, 40);
        </script>
    </body>
    </html>
    '''

@app.route('/ig-extract')
def extract_instagram():
    user_key = request.args.get('key')
    
    # Professional Access Denied Page
    if user_key != MY_OWN_API_SECURE_KEY:
        error_content = '''
        <p>CRITICAL ERROR: INVALID_API_KEY</p>
        <pre>{
  "status": "error",
  "status_code": 401,
  "message": "Access Denied! Please provide a valid key."
}</pre>
        <p>Your IP has been logged for security purposes.</p>
        '''
        return render_template_string(get_matrix_template("Access Denied", "System Authentication Failed", error_content, is_error=True)), 401

    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "status_code": 400, "message": "Username missing."}), 400

    headers = {"Content-Type": "application/json", "x-api-key": HASDATA_API_KEY}
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            full_data = response.json()
            filtered_output = {
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
            pretty_json = json.dumps(filtered_output, indent=2, ensure_ascii=False)
            
            # Success Data Page
            success_content = f'''
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-size:12px;">STATUS: 200 OK</span>
                <button onclick="copyData()" style="background:transparent; color:#0f0; border:1px solid #0f0; cursor:pointer;">COPY</button>
            </div>
            <pre id="json-data" style="text-align:left; background:rgba(0,30,0,0.5); padding:10px; color:#0f0; border:1px solid #030;">{pretty_json}</pre>
            <script>function copyData() {{ const t = document.getElementById('json-data').innerText; navigator.clipboard.writeText(t); alert('Copied!'); }}</script>
            '''
            return render_template_string(get_matrix_template("Data Extracted", "Instagram Data Securely Fetched", success_content))
        
        else:
            return jsonify({"status": "error", "message": "Extraction failed"}), response.status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    # Main Landing Page
    home_content = "<p>Welcome to TeamExe Secure Instagram Scraper. Please use your API Key to access the data endpoint.</p><p>Telegram: @Configexe</p>"
    return render_template_string(get_matrix_template("Teamexe Insta API", "TEAMEXE SECURE IG SCRAPER", home_content))

app = app
    
