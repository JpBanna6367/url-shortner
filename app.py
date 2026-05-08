from flask import Flask, request, render_template_string, redirect
import random
import string
import json
import os

app = Flask(__name__)
DB_FILE = "links.json"

# ======================= HELPERS =======================
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, 'w') as f: json.dump(db, f)

def gen_code():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

# ======================= HOME PAGE =======================
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Link Unlocker - Shorten URL</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a1a; color: #fff; font-family: 'Segoe UI', Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .header { text-align: center; padding: 30px 0; }
        .header h1 { font-size: 36px; color: #00ff9d; }
        .container { background: #111133; border-radius: 15px; padding: 30px; max-width: 600px; width: 100%; border: 1px solid #00ff9d33; }
        input { width: 100%; padding: 15px; background: #0a0a1a; border: 1px solid #00ff9d44; border-radius: 10px; color: #fff; font-size: 16px; margin-bottom: 15px; }
        input:focus { outline: none; border-color: #00ff9d; }
        .btn { background: linear-gradient(135deg, #00ff9d, #00bfff); color: #000; border: none; padding: 12px 30px; font-size: 16px; font-weight: bold; border-radius: 50px; cursor: pointer; }
        .result { background: #000; border: 2px dashed #00ff9d; border-radius: 10px; padding: 15px; margin-top: 20px; word-break: break-all; font-size: 18px; color: #00ff9d; display: none; }
        .copy-btn { background: #00ff9d22; color: #00ff9d; border: 1px solid #00ff9d44; padding: 8px 20px; border-radius: 20px; cursor: pointer; margin-top: 10px; display: none; }
        .footer { color: #555; font-size: 12px; margin-top: 30px; text-align: center; }
    </style>
</head>
<body>
    <div class="header"><h1>🔗 Link Unlocker</h1><p style="color:#888;">Shorten your link with ads</p></div>
    <div class="container">
        <form method="POST" action="/">
            <input type="url" name="url" placeholder="Paste your long URL here..." required>
            <button type="submit" class="btn">🚀 Create Link</button>
        </form>
        {% if show %}
        <div class="result" id="resultBox"><strong>🔗 Your Link:</strong> {{ short_url }}</div>
        <button class="copy-btn" id="copyBtn" onclick="copyLink('{{ short_url }}')">📋 Copy Link</button>
        {% endif %}
    </div>
    <div class="footer">Powered by <a href="https://t.me/eaglescrip" style="color:#00bfff;">@eaglescrip</a></div>
    <script>
        {% if show %}
        document.getElementById('resultBox').style.display = 'block';
        document.getElementById('copyBtn').style.display = 'inline-block';
        {% endif %}
        function copyLink(u){ navigator.clipboard.writeText(u); alert('✅ Link copied!'); }
    </script>
</body>
</html>
"""

# ======================= PAGE 1 =======================
PAGE1_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Step 1/3 - Unlock Link</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a1a; color: #fff; font-family: 'Segoe UI', Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 10px; }
        .container { max-width: 500px; width: 100%; text-align: center; }
        .header { background: #111133; padding: 15px; border-radius: 15px 15px 0 0; border: 1px solid #00ff9d33; }
        .header h2 { color: #00ff9d; }
        .progress { color: #888; margin: 10px 0; }
        .ad-box1 { background: #ffffff05; border: 1px solid #ffffff10; border-radius: 10px; padding: 5px; margin: 10px 0; min-height: 100px; }
        .ad-box2 { background: #ffffff05; border: 1px solid #ffffff10; border-radius: 10px; padding: 5px; margin: 10px 0; min-height: 300px; }
        .timer { color: #ffcc00; font-size: 24px; margin: 15px 0; }
        .btn { background: #00ff9d; color: #000; border: none; padding: 12px 40px; font-size: 16px; font-weight: bold; border-radius: 50px; cursor: pointer; display: none; }
        .btn:hover { background: #00cc7d; }
        .footer { color: #555; font-size: 12px; margin-top: 15px; }
        .footer a { color: #00bfff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h2>🔓 Unlock Link</h2></div>
        <div class="progress">Step 1 of 3</div>
        
        <!-- Popunder Ad -->
        <script src="https://pl29375092.profitablecpmratenetwork.com/3c/7f/f6/3c7ff61c624a250b67b68829b8f3930f.js"></script>
        
        <!-- Banner Ad 300x250 -->
        <div class="ad-box1">
            <script>atOptions={'key':'f8bb57d798403e9f370354dcca00dc3a','format':'iframe','height':250,'width':300,'params':{}};</script>
            <script src="https://www.highperformanceformat.com/f8bb57d798403e9f370354dcca00dc3a/invoke.js"></script>
        </div>
        
        <div class="timer" id="timer">⏳ Wait 10 seconds...</div>
        <button class="btn" id="continueBtn" onclick="location.href='/go/{{ code }}/2'">➡️ Continue to Step 2</button>
    </div>
    <div class="footer">Powered by <a href="https://t.me/eaglescrip">@eaglescrip</a></div>
    
    <script>
        var timeLeft = 10;
        var timer = setInterval(function() {
            timeLeft--;
            document.getElementById('timer').textContent = '⏳ Wait ' + timeLeft + ' seconds...';
            if (timeLeft <= 0) {
                clearInterval(timer);
                document.getElementById('timer').textContent = '✅ Ready!';
                document.getElementById('continueBtn').style.display = 'block';
            }
        }, 1000);
    </script>
</body>
</html>
"""

# ======================= PAGE 2 =======================
PAGE2_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Step 2/3 - Unlock Link</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a1a; color: #fff; font-family: 'Segoe UI', Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 10px; }
        .container { max-width: 500px; width: 100%; text-align: center; }
        .header { background: #111133; padding: 15px; border-radius: 15px 15px 0 0; border: 1px solid #00ff9d33; }
        .header h2 { color: #00ff9d; }
        .progress { color: #888; margin: 10px 0; }
        .ad-box { background: #ffffff05; border: 1px solid #ffffff10; border-radius: 10px; padding: 5px; margin: 10px 0; min-height: 250px; }
        .timer { color: #ffcc00; font-size: 24px; margin: 15px 0; }
        .btn { background: #ff6600; color: #fff; border: none; padding: 12px 40px; font-size: 16px; font-weight: bold; border-radius: 50px; cursor: pointer; display: none; }
        .btn:hover { background: #cc5500; }
        .footer { color: #555; font-size: 12px; margin-top: 15px; }
        .footer a { color: #00bfff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h2>🔓 Almost There!</h2></div>
        <div class="progress">Step 2 of 3</div>
        
        <!-- Popup Ad (opens on page load) -->
        <script async="async" data-cfasync="false" src="https://pl29375093.profitablecpmratenetwork.com/de19afb79a8c9fd0ffd9b97a2eda8759/invoke.js"></script>
        <div id="container-de19afb79a8c9fd0ffd9b97a2eda8759"></div>
        
        <!-- Skyscraper Ad 160x300 -->
        <div class="ad-box">
            <script>atOptions={'key':'51430222ac465eed7b058dba71a2df22','format':'iframe','height':300,'width':160,'params':{}};</script>
            <script src="https://www.highperformanceformat.com/51430222ac465eed7b058dba71a2df22/invoke.js"></script>
        </div>
        
        <div class="timer" id="timer">⏳ Wait 10 seconds...</div>
        <button class="btn" id="continueBtn" onclick="location.href='/go/{{ code }}/3'">➡️ Continue to Step 3</button>
    </div>
    <div class="footer">Powered by <a href="https://t.me/eaglescrip">@eaglescrip</a></div>
    
    <script>
        var timeLeft = 10;
        var timer = setInterval(function() {
            timeLeft--;
            document.getElementById('timer').textContent = '⏳ Wait ' + timeLeft + ' seconds...';
            if (timeLeft <= 0) {
                clearInterval(timer);
                document.getElementById('timer').textContent = '✅ Ready!';
                document.getElementById('continueBtn').style.display = 'block';
            }
        }, 1000);
    </script>
</body>
</html>
"""

# ======================= PAGE 3 =======================
PAGE3_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Step 3/3 - Unlock Link</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a1a; color: #fff; font-family: 'Segoe UI', Arial, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 10px; }
        .container { max-width: 500px; width: 100%; text-align: center; }
        .header { background: #111133; padding: 15px; border-radius: 15px 15px 0 0; border: 1px solid #00ff9d33; }
        .header h2 { color: #00ff9d; }
        .progress { color: #888; margin: 10px 0; }
        .ad-box { background: #ffffff05; border: 1px solid #ffffff10; border-radius: 10px; padding: 5px; margin: 10px 0; min-height: 600px; }
        .timer { color: #ffcc00; font-size: 24px; margin: 15px 0; }
        .btn { background: linear-gradient(135deg, #ff0088, #6600ff); color: #fff; border: none; padding: 15px 50px; font-size: 18px; font-weight: bold; border-radius: 50px; cursor: pointer; display: none; }
        .btn:hover { transform: scale(1.05); }
        .footer { color: #555; font-size: 12px; margin-top: 15px; }
        .footer a { color: #00bfff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h2>🎉 Final Step!</h2></div>
        <div class="progress">Step 3 of 3</div>
        
        <!-- Popup Ad -->
        <script src="https://pl29375092.profitablecpmratenetwork.com/3c/7f/f6/3c7ff61c624a250b67b68829b8f3930f.js"></script>
        
        <!-- Large Skyscraper 160x600 -->
        <div class="ad-box">
            <script>atOptions={'key':'600ba50e4e3d0dea128e22dc363f57d6','format':'iframe','height':600,'width':160,'params':{}};</script>
            <script src="https://www.highperformanceformat.com/600ba50e4e3d0dea128e22dc363f57d6/invoke.js"></script>
        </div>
        
        <div class="timer" id="timer">⏳ Wait 10 seconds...</div>
        <button class="btn" id="continueBtn" onclick="location.href='/unlock/{{ code }}'">🎯 Get Link Now!</button>
    </div>
    <div class="footer">Powered by <a href="https://t.me/eaglescrip">@eaglescrip</a></div>
    
    <script>
        var timeLeft = 10;
        var timer = setInterval(function() {
            timeLeft--;
            document.getElementById('timer').textContent = '⏳ Wait ' + timeLeft + ' seconds...';
            if (timeLeft <= 0) {
                clearInterval(timer);
                document.getElementById('timer').textContent = '✅ Ready!';
                document.getElementById('continueBtn').style.display = 'block';
            }
        }, 1000);
    </script>
</body>
</html>
"""

# ======================= ROUTES =======================
@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = ""; show = False
    if request.method == 'POST':
        long_url = request.form.get('url', '')
        if long_url:
            db = load_db()
            code = gen_code()
            db[code] = long_url
            save_db(db)
            base = request.host_url.rstrip('/')
            short_url = f"{base}/go/{code}/1"
            show = True
    return render_template_string(HOME_TEMPLATE, short_url=short_url, show=show)

@app.route('/go/<code>/1')
def page1(code):
    return render_template_string(PAGE1_TEMPLATE, code=code)

@app.route('/go/<code>/2')
def page2(code):
    return render_template_string(PAGE2_TEMPLATE, code=code)

@app.route('/go/<code>/3')
def page3(code):
    return render_template_string(PAGE3_TEMPLATE, code=code)

@app.route('/unlock/<code>')
def unlock(code):
    db = load_db()
    original_url = db.get(code)
    if original_url:
        return redirect(original_url)
    return "Link not found!", 404

@app.route('/api/create', methods=['POST'])
def api_create():
    long_url = request.json.get('url', '')
    if not long_url:
        return {"error": "URL required"}, 400
    db = load_db()
    code = gen_code()
    db[code] = long_url
    save_db(db)
    base = request.host_url.rstrip('/')
    return {"url": f"{base}/go/{code}/1", "code": code}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
