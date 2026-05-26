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
    """Generates the original Matrix UI with professional fixes."""
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
                padding: 25px; border-radius: 15px; box-shadow: 0 0 25px {shadow_color};
                width: 92%; max-width: 420px; text-align: center; position: relative;
            }}
            
            h2 {{ 
                border-bottom: 1px solid {border_color}; padding-bottom: 15px; 
                font-family: 'Press Start 2P', cursive; font-size: 13px; 
                line-height: 1.6; letter-spacing: 1px; margin-top: 0;
            }}
            
            .header-info {{
                display: flex; justify-content: space-between; align-items: center;
                margin: 15px 0 10px 0; font-size: 11px;
            }}

            .message {{ font-size: 15px; margin: 20px 0; line-height: 1.5; color: #fff; }}
            
            pre {{ 
                text-align: left; background: rgba(0, 15, 0, 0.9); 
                padding: 15px; border-radius: 8px; color: {text_color}; 
                font-size: 12px; white-space: pre-wrap; word-wrap: break-word;
                border: 1px solid rgba({ '255, 0, 0' if is_error else '0, 255, 0' }, 0.3);
                margin: 0 0 20px 0; max-height: 250px; overflow-y: auto;
            }}

            .notice-box {{
                border: 1px solid {border_color}; background: rgba({ '255, 0, 0' if is_error else '0, 255, 0' }, 0.1);
                color: {border_color}; padding: 10px; font-size: 11px; font-weight: bold;
                margin-bottom: 20px; text-transform: uppercase;
            }}

            .copy-btn {{
                background: transparent; border: 1px solid {border_color}; 
                color: {border_color}; padding: 6px 12px; cursor: pointer; 
                font-family: 'Share Tech Mono', monospace; font-size: 11px;
                border-radius: 4px; transition: 0.2s;
            }}
            .copy-btn:hover {{ background: {border_color}; color: #000; font-weight: bold; }}

            .btn-dev {{
                display: block; width: 100%; padding: 15px; 
                background: {border_color}; color: #000; text-decoration: none; 
                font-weight: bold; border-radius: 8px; font-size: 14px;
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
                alert('JSON Data Copied to Clipboard!');
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/ig-extract')
def extract_instagram():
    user_key = request.args.get('key')
    
    # Error with red notice box restored
    if user_key != MY_OWN_API_SECURE_KEY:
        error_json = json.dumps({"status": "error", "code": 401, "message": "Invalid Security Key"}, indent=2)
        error_content = f'''
        <div class="header-info">
            <span>ERROR: AUTH_FAILED</span>
            <button class="copy-btn" onclick="copyData()">COPY JSON</button>
        </div>
        <pre id="json-output">{error_json}</pre>
        <div class="notice-box">
            NOTICE: ACCESS DENIED! CONTACT DEVELOPER ON TELEGRAM TO PURCHASE A PRIVATE API KEY.
        </div>
        '''
        return render_template_string(get_matrix_template("401 Unauthorized", "Security Alert", error_content, is_error=True)), 401

    username = request.args.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Username missing"}), 400

    headers = {"Content-Type": "application/json", "x-api-key": HASDATA_API_KEY}
    params = {"handle": username}

    try:
        response = requests.get(HASDATA_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            full_data = response.json()
            # Fixed dictionary structure to avoid "unhashable type" error
            filtered_output = {
                "status": "success",
                "developer": "@Configexe",
                "data": {
                    "biography": full_data.get("biography"),
                    "followersCount": full_data.get("followersCount"),
                    "fullName": full_data.get("fullName"),
                    "id": full_data.get("id"),
                    "fbid": full_data.get("fbid")
                }
            }
            pretty_json = json.dumps(filtered_output, indent=2, ensure_ascii=False)
            
            success_content = f'''
            <div class="header-info">
                <span>PROTOCOL: SECURE DATA</span>
                <button class="copy-btn" onclick="copyData()">COPY JSON</button>
            </div>
            <pre id="json-output">{pretty_json}</pre>
            <div class="notice-box">
                UPGRADE: INTERESTED IN A PRIVATE API KEY? CONTACT THE DEVELOPER ON TELEGRAM.
            </div>
            '''
            return render_template_string(get_matrix_template("Success", "Data Extracted Successfully", success_content))
        return jsonify({"error": "API Error"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    home_content = '''
    <p>Teamexe Secure Instagram API is online and fully functional.</p>
    <div class="notice-box">
        API LICENSING: WANT TO PURCHASE YOUR OWN API KEY? REACH OUT ON TELEGRAM.
    </div>
    '''
    return render_template_string(get_matrix_template("Teamexe API", "SYSTEM STATUS: ACTIVE", home_content))

app = app
    
