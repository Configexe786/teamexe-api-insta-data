from flask import Flask, request, jsonify, render_template_string, redirect, session
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "TEAMEXE_SUPER_SECRET_SESSION_KEY"

# Config
HASDATA_API_KEY = "fe8ccbd8-88d3-44dd-bf51-390a180d1ed0"
HASDATA_URL = "https://api.hasdata.com/scrape/instagram/profile"

# Admin Credentials
ADMIN_EMAIL = "tgmastergaming@gmail.com"
ADMIN_PASS = "Teamexe@admin786"

# Temporary Key Store (In production, use Supabase/MongoDB)
# Format: "key": {"expiry": datetime, "daily_limit": int, "total_limit": int, "used_today": int, "total_used": int}
valid_keys = {
    "TEAMEXE786": {
        "expiry": datetime.now() + timedelta(days=30),
        "daily_limit": 50,
        "total_limit": 1000,
        "used_today": 5,
        "total_used": 10
    }
}

def get_matrix_template(title, heading, content, is_error=False, show_contact=True):
    border_color = "#f00" if is_error else "#0f0"
    text_color = "#ff3333" if is_error else "#0f0"
    shadow_color = "rgba(255, 0, 0, 0.7)" if is_error else "rgba(0, 255, 0, 0.7)"
    
    contact_btn = f'<a href="https://t.me/configexe" class="btn-dev">Contact Developer</a>' if show_contact else ''
    
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
            body {{ margin: 0; padding: 0; background: black; font-family: 'Share Tech Mono', monospace; color: {text_color}; min-height: 100vh; display: flex; align-items: center; justify-content: center; }}
            canvas {{ position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.4; }}
            .container {{ background: rgba(0, 5, 0, 0.95); border: 2px solid {border_color}; padding: 25px; border-radius: 15px; box-shadow: 0 0 25px {shadow_color}; width: 92%; max-width: 450px; text-align: center; position: relative; z-index: 1; }}
            h2 {{ border-bottom: 1px solid {border_color}; padding-bottom: 15px; font-family: 'Press Start 2P', cursive; font-size: 12px; line-height: 1.6; margin-top: 0; }}
            pre {{ text-align: left; background: rgba(0, 15, 0, 0.9); padding: 15px; border-radius: 8px; color: {text_color}; font-size: 11px; white-space: pre-wrap; border: 1px solid rgba(0, 255, 0, 0.3); margin-bottom: 15px; max-height: 200px; overflow-y: auto; }}
            .stats-box {{ border: 1px solid {border_color}; background: rgba(0, 255, 0, 0.05); padding: 10px; font-size: 10px; text-align: left; margin-bottom: 15px; }}
            .btn-dev {{ display: block; width: 100%; padding: 12px; background: {border_color}; color: #000; text-decoration: none; font-weight: bold; border-radius: 8px; font-size: 13px; margin-top: 10px; border: none; cursor: pointer; }}
            input {{ width: 100%; padding: 10px; margin: 10px 0; background: #000; border: 1px solid {border_color}; color: {text_color}; font-family: 'Share Tech Mono'; }}
        </style>
    </head>
    <body>
        <canvas id="matrix"></canvas>
        <div class="container">
            <h2>{heading}</h2>
            <div class="content">{content}</div>
            {contact_btn}
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
        </script>
    </body>
    </html>
    '''

# --- Admin Panel Routes ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('email') == ADMIN_EMAIL and request.form.get('password') == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect('/admin/dashboard')
        return render_template_string(get_matrix_template("Login Failed", "AUTH ERROR", "<p>Invalid Admin Credentials</p>", True))
    
    login_form = '''
    <form method="POST">
        <input type="email" name="email" placeholder="Admin Email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit" class="btn-dev">LOGIN TO PANEL</button>
    </form>
    '''
    return render_template_string(get_matrix_template("Admin Login", "SECURE ADMIN LOGIN", login_form, False, False))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): return redirect('/admin')
    
    keys_list = ""
    for k, v in valid_keys.items():
        keys_list += f"<li>{k} (Exp: {v['expiry'].strftime('%Y-%m-%d')}) <a href='/admin/delete/{k}' style='color:red'>[Delete]</a></li>"
    
    content = f'''
    <div style="text-align:left; font-size:12px;">
        <h3>Create New Key</h3>
        <form action="/admin/add" method="POST">
            <input type="text" name="key" placeholder="Key (6-12 chars)" minlength="6" maxlength="12" required>
            <input type="number" name="days" placeholder="Expiry Days" required>
            <input type="number" name="daily" placeholder="Daily Limit" required>
            <input type="number" name="total" placeholder="Total Limit" required>
            <button type="submit" class="btn-dev">GENERATE KEY</button>
        </form>
        <h3>Active Keys</h3>
        <ul style="list-style:none; padding:0;">{keys_list}</ul>
        <a href="/admin/logout" class="btn-dev" style="background:#444; color:#fff">LOGOUT</a>
    </div>
    '''
    return render_template_string(get_matrix_template("Dashboard", "ADMIN CONTROL PANEL", content, False, False))

@app.route('/admin/add', methods=['POST'])
def add_key():
    if not session.get('admin_logged_in'): return redirect('/admin')
    key = request.form.get('key')
    days = int(request.form.get('days'))
    valid_keys[key] = {
        "expiry": datetime.now() + timedelta(days=days),
        "daily_limit": int(request.form.get('daily')),
        "total_limit": int(request.form.get('total')),
        "used_today": 0, "total_used": 0
    }
    return redirect('/admin/dashboard')

@app.route('/admin/delete/<key>')
def delete_key(key):
    if not session.get('admin_logged_in'): return redirect('/admin')
    if key in valid_keys: del valid_keys[key]
    return redirect('/admin/dashboard')

@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin')

# --- Main API Route ---
@app.route('/ig-extract')
def extract_instagram():
    user_key = request.args.get('key')
    
    if user_key not in valid_keys:
        return render_template_string(get_matrix_template("401", "ACCESS DENIED", "<p>Invalid or Expired API Key</p>", True))

    key_data = valid_keys[user_key]
    
    # Expiry Check
    time_left = key_data['expiry'] - datetime.now()
    if time_left.total_seconds() <= 0:
        return render_template_string(get_matrix_template("Expired", "KEY EXPIRED", "<p>Your license has expired.</p>", True))

    # Limit Check
    if key_data['used_today'] >= key_data['daily_limit']:
        return render_template_string(get_matrix_template("Limit", "DAILY LIMIT REACHED", "<p>Please wait until tomorrow.</p>", True))

    username = request.args.get('username')
    if not username: return jsonify({"error": "Username missing"}), 400

    # Logic to Scrape
    try:
        response = requests.get(HASDATA_URL, headers={"x-api-key": HASDATA_API_KEY}, params={"handle": username})
        if response.status_code == 200:
            # Update Usage
            valid_keys[user_key]['used_today'] += 1
            valid_keys[user_key]['total_used'] += 1
            
            # Format remaining time
            hours, remainder = divmod(int(time_left.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            stats_html = f'''
            <div class="stats-box">
                <b>KEY STATUS:</b> VALID<br>
                <b>EXPIRY IN:</b> {time_left.days}d {hours % 24}h {minutes}m {seconds}s<br>
                <b>DAILY USAGE:</b> {valid_keys[user_key]['used_today']}/{key_data['daily_limit']}<br>
                <b>TOTAL QUOTA:</b> {valid_keys[user_key]['total_used']}/{key_data['total_limit']}
            </div>
            '''
            
            pretty_json = json.dumps(response.json(), indent=2)
            content = f'<pre>{pretty_json}</pre>{stats_html}'
            return render_template_string(get_matrix_template("Success", "DATA EXTRACTED", content))
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return render_template_string(get_matrix_template("Teamexe API", "SYSTEM STATUS: ACTIVE", "<p>API is Online. Authentication Required.</p>"))
    
