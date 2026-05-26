from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# HasData Configuration
HASDATA_API_KEY = "fe8ccbd8-88d3-44dd-bf51-390a180d1ed0"
HASDATA_URL = "https://api.hasdata.com/scrape/instagram/profile"

# API Security Configuration
MY_OWN_API_SECURE_KEY = "TEAMEXE786" 

def get_matrix_template(title, heading, content, is_error=False):
    """Generates a perfectly centered Matrix-themed UI with fixed copy button."""
    border_color = "#f00" if is_error else "#0f0"
    text_color = "#ff3333" if is_error else "#0f0"
    shadow_color = "rgba(255, 0, 0, 0.7)" if is_error else "rgba(0, 255, 0, 0.7)"
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; }}
            body {{ 
                margin: 0; padding: 0; background: black; 
                font-family: 'Share Tech Mono', monospace; 
                color: {text_color}; height: 100vh;
                display: flex; align-items: center; justify-content: center; overflow: hidden;
            }}
            canvas {{ position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.4; }}
            
            .container {{
                background: rgba(0, 5, 0, 0.95); border: 2px solid {border_color};
                padding: 25px; border-radius: 12px; box-shadow: 0 0 25px {shadow_color};
                width: 92%; max-width: 420px; text-align: center; position: relative;
            }}
            
            h2 {{ 
                border-bottom: 1px solid {border_color}; padding-bottom: 15px; 
                font-family: 'Press Start 2P', cursive; font-size: 13px; 
                line-height: 1.6; letter-spacing: 1px; margin-top: 0;
            }}
            
            .header-info {{
                display: flex; justify-content: space-between; align-items: center;
                margin: 15px 0 10px 0; font-size: 10px; text-transform: uppercase;
            }}

            .message {{ font-size: 14px; margin: 15px 0; line-height: 1.5; color: #fff; }}
            
            /* Professional JSON Box */
            .json-wrapper {{ position: relative; margin-top: 10px; }}
            
            pre {{ 
                text-align: left; background: rgba(0, 15, 0, 0.9); 
                padding: 15px; border-radius: 6px; color: {text_color}; 
                font-size: 12px; white-space: pre-wrap; word-wrap: break-word;
                border: 1px solid rgba({ '255,0,0' if is_error else '0,255,0' }, 0.3);
                margin: 0 0 20px 0; max-height: 220px; overflow-y: auto;
            }}

            /* Clean Copy Button */
            .copy-btn {{
                background: transparent; border: 1px solid {border_color}; 
                color: {border_color}; padding: 5px 12px; cursor: pointer; 
                font-family: 'Share Tech Mono', monospace; font-size: 11px;
                border-radius: 3px; transition: 0.2s;
            }}
            .copy-btn:hover {{ background: {border_color}; color: #000; font-weight: bold; }}

            .btn-dev {{
                display: block; width: 100%; padding: 15px; 
                background: {border_color}; color: #000; text-decoration: none; 
                font-weight: bold; border-radius: 6px; font-size: 14px;
                box-shadow: 0 0 15px {shadow_color}; border: none; text-transform: uppercase;
            }}
        </style>
    </head>
    <body>
        <canvas id="matrix"></canvas>
        <div class="container">
            <h2>{heading}</h2>
            <div class="message">{content}</div>
            <a href="https://t.me/configexe" class="btn-dev">Contact Developer</a>
        </div>
        <script>
            const canvas = document.getElementById('matrix');
            const ctx = canvas.getContext('2d');
            function resize() {{ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }}
            window.onresize = resize; resize();
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
            setInterval(draw, 45);
            function copyData() {{
                const text = document.getElementById('json-output').innerText;
                navigator.clipboard.writeText(text);
                const btn = document.querySelector('.copy-btn');
                btn.innerText = 'COPIED!';
                setTimeout(() => {{ btn.innerText = 'COPY JSON'; }}, 2000);
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/ig-extract')
def extract_instagram():
    user_key = request.args.get('key')
    
    # Unauthorized Access with Copy Button
    if user_key != MY_OWN_API_SECURE_KEY:
        error_json = json.dumps({"status": "error", "code": 401, "message": "Invalid Security Key"}, indent=2)
        error_content = f'''
        <p style="color:#ff4444; font-weight:bold; margin-bottom:5px;">ACCESS DENIED: UNAUTHORIZED</p>
        <div class="header-info">
            <span>TYPE: AUTH_ERROR</span>
            <button class="copy-btn" onclick="copyData()">COPY JSON</button>
        </div>
        <pre id="json-output">{error_json}</pre>
        <p>A private license key is required to access this endpoint. Please contact the official developer on Telegram to purchase a valid API key.</p>
        '''
        return render_template_string(get_matrix_template("401 Unauthorized", "Security Alert", error_content, is_error=True)), 401

    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Username parameter is missing."}), 400

    headers = {"Content-Type": "application/json", "x-api-key": HASDATA_API_KEY}
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            full_data = response.json()
            filtered_output = {{
                "status": "success", "status_code": 200, "developer": "@Configexe",
                "data": {{ "fullName": full_data.get("fullName"), "followers": full_data.get("followersCount"), "bio": full_data.get("biography") }}
            }}
            pretty_json = json.dumps(filtered_output, indent=2, ensure_ascii=False)
            
            # Success Page with Professional Copy Button
            success_content = f'''
            <div class="header-info">
                <span>PROTOCOL: SECURE | AES-256</span>
                <button class="copy-btn" onclick="copyData()">COPY JSON</button>
            </div>
            <pre id="json-output">{pretty_json}</pre>
            '''
            return render_template_string(get_matrix_template("Success", "Data Extracted Successfully", success_content))
        else:
            return jsonify({{"status": "error", "message": "API error"}}), 500
    except Exception as e:
        return jsonify({{"status": "error", "message": str(e)}}), 500

@app.route('/')
def home():
    home_content = '<p>Teamexe Secure Instagram API is online.</p>'
    return render_template_string(get_matrix_template("Home", "SYSTEM STATUS: ACTIVE", home_content))

app = app
    
