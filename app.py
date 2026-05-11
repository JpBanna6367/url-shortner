# shorturl_server.py - Working Short URL Generator

from flask import Flask, request, render_template_string, redirect, jsonify
import random
import string
import json
import os

app = Flask(__name__)
DB_FILE = "urls.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

def generate_code():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

# ======================= MAIN PAGE =======================
HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Short URL Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            width: 90%;
            max-width: 550px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 10px; }
        .sub { color: #666; margin-bottom: 30px; }
        input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .generate-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
        }
        .result-box {
            margin-top: 30px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
            display: none;
        }
        .short-url {
            background: white;
            padding: 12px;
            border-radius: 8px;
            font-size: 18px;
            color: #667eea;
            word-break: break-all;
            margin-bottom: 15px;
            border: 1px solid #ddd;
        }
        .copy-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
        }
        .copy-btn:hover { background: #218838; }
        .footer { margin-top: 20px; font-size: 12px; color: #aaa; }
        .loading { display: none; margin-top: 20px; color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Short URL Generator</h1>
        <p class="sub">Paste your long URL and get a short link</p>
        
        <input type="url" id="longUrl" placeholder="https://example.com/your-very-long-url">
        <button class="generate-btn" onclick="generateShortUrl()">✨ Generate Short URL</button>
        
        <div class="loading" id="loading">⏳ Generating...</div>
        
        <div class="result-box" id="resultBox">
            <p style="margin-bottom: 10px;">✅ Your Short URL:</p>
            <div class="short-url" id="shortUrl"></div>
            <button class="copy-btn" onclick="copyToClipboard()">📋 Copy to Clipboard</button>
            <p class="footer">⚠️ Copy this link and open in browser</p>
        </div>
        
        <div class="footer">
            Powered by ShortURL
        </div>
    </div>
    
    <script>
        async function generateShortUrl() {
            const longUrl = document.getElementById('longUrl').value.trim();
            
            if (!longUrl) {
                alert('Please enter a URL');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('resultBox').style.display = 'none';
            
            try {
                const response = await fetch('/api/shorten', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: longUrl })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('shortUrl').textContent = data.short_url;
                    document.getElementById('resultBox').style.display = 'block';
                    document.getElementById('longUrl').value = '';
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function copyToClipboard() {
            const url = document.getElementById('shortUrl').textContent;
            navigator.clipboard.writeText(url).then(() => {
                alert('✅ URL copied to clipboard!');
            }).catch(() => {
                alert('❌ Failed to copy');
            });
        }
    </script>
</body>
</html>
"""

# ======================= PAGE 1 =======================
PAGE1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Please Wait - Step 1/3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 100%);
            font-family: 'Segoe UI', Arial, sans-serif;
            min-height: 100vh;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .timer-box {
            background: rgba(0,0,0,0.5);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            border: 2px solid #00ff9d;
        }
        .timer { font-size: 60px; font-weight: bold; color: #00ff9d; }
        .large-banner {
            background: #111133;
            border-radius: 15px;
            padding: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .small-banner {
            background: #111133;
            border-radius: 10px;
            padding: 8px;
            margin: 10px 0;
            text-align: center;
        }
        .next-btn {
            background: linear-gradient(135deg, #00ff9d, #00bfff);
            color: #000;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            width: 100%;
            margin: 20px 0;
            display: none;
        }
        .footer { text-align: center; padding: 20px; color: #555; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="timer-box">
            <div class="timer" id="timer">10</div>
        </div>
        
        <div class="large-banner">
            <script>
                atOptions = {
                    'key' : '9ae6bef8d83530cbbb39510089116235',
                    'format' : 'iframe',
                    'height' : 90,
                    'width' : 728,
                    'params' : {}
                };
            </script>
            <script src="https://www.highperformanceformat.com/9ae6bef8d83530cbbb39510089116235/invoke.js"></script>
        </div>
        
        <div class="small-banner">
            <script>
                atOptions = {
                    'key' : '9ae6bef8d83530cbbb39510089116235',
                    'format' : 'iframe',
                    'height' : 50,
                    'width' : 320,
                    'params' : {}
                };
            </script>
            <script src="https://www.highperformanceformat.com/9ae6bef8d83530cbbb39510089116235/invoke.js"></script>
        </div>
        
        <button class="next-btn" id="nextBtn" onclick="location.href='/page2/{{ code }}'">➡️ NEXT PAGE</button>
    </div>
    
    <script>
        let timeLeft = 10;
        const timerEl = document.getElementById('timer');
        const nextBtn = document.getElementById('nextBtn');
        
        const timerInterval = setInterval(function() {
            timeLeft--;
            timerEl.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                timerEl.textContent = '✅ GO';
                nextBtn.style.display = 'block';
            }
        }, 1000);
    </script>
</body>
</html>
"""

# ======================= PAGE 2 =======================
PAGE2 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Please Wait - Step 2/3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 100%);
            font-family: 'Segoe UI', Arial, sans-serif;
            min-height: 100vh;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .timer-box {
            background: rgba(0,0,0,0.5);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            border: 2px solid #ff6600;
        }
        .timer { font-size: 60px; font-weight: bold; color: #ff6600; }
        .large-banner {
            background: #111133;
            border-radius: 15px;
            padding: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .small-banner {
            background: #111133;
            border-radius: 10px;
            padding: 8px;
            margin: 10px 0;
            text-align: center;
        }
        .next-btn {
            background: linear-gradient(135deg, #ff6600, #ff0088);
            color: #fff;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            width: 100%;
            margin: 20px 0;
            display: none;
        }
        .footer { text-align: center; padding: 20px; color: #555; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="timer-box">
            <div class="timer" id="timer">8</div>
        </div>
        
        <div class="large-banner">
            <script>
                atOptions = {
                    'key' : '9ae6bef8d83530cbbb39510089116235',
                    'format' : 'iframe',
                    'height' : 90,
                    'width' : 728,
                    'params' : {}
                };
            </script>
            <script src="https://www.highperformanceformat.com/9ae6bef8d83530cbbb39510089116235/invoke.js"></script>
        </div>
        
        <div class="small-banner">
            <script>
                atOptions = {
                    'key' : '9ae6bef8d83530cbbb39510089116235',
                    'format' : 'iframe',
                    'height' : 50,
                    'width' : 320,
                    'params' : {}
                };
            </script>
            <script src="https://www.highperformanceformat.com/9ae6bef8d83530cbbb39510089116235/invoke.js"></script>
        </div>
        
        <button class="next-btn" id="nextBtn" onclick="location.href='/page3/{{ code }}'">➡️ NEXT PAGE</button>
    </div>
    
    <script>
        let timeLeft = 8;
        const timerEl = document.getElementById('timer');
        const nextBtn = document.getElementById('nextBtn');
        
        const timerInterval = setInterval(function() {
            timeLeft--;
            timerEl.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                timerEl.textContent = '✅ GO';
                nextBtn.style.display = 'block';
            }
        }, 1000);
    </script>
</body>
</html>
"""

# ======================= PAGE 3 =======================
PAGE3 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Your Link - Step 3/3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a1a, #1a1a3a);
            font-family: 'Segoe UI', Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        h1 { color: #00ff9d; margin-bottom: 20px; }
        .get-link-btn {
            background: linear-gradient(135deg, #ff0088, #6600ff);
            color: white;
            border: none;
            padding: 18px 40px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
        }
        .support-btn {
            background: #ff6600;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 50px;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
        }
        .warning { color: #ff6600; font-size: 12px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Your Link is Ready!</h1>
        <button class="get-link-btn" onclick="getLink()">🔗 GET LINK</button>
        <button class="support-btn" onclick="supportClick()">💪 SUPPORT US</button>
        <p class="warning">⚠️ Click "GET LINK" to continue</p>
    </div>
    
    <script>
        let popunderOpened = false;
        let finalUrl = '{{ final_url }}';
        
        function getLink() {
            if (!popunderOpened) {
                window.open('https://pl29414129.profitablecpmratenetwork.com/click', '_blank');
                popunderOpened = true;
                setTimeout(() => {
                    window.location.href = finalUrl;
                }, 1000);
            } else {
                window.location.href = finalUrl;
            }
        }
        
        function supportClick() {
            window.open('https://pl29414129.profitablecpmratenetwork.com/click', '_blank');
            alert('Thank you for your support!');
        }
    </script>
</body>
</html>
"""

# ======================= ROUTES =======================
@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    try:
        data = request.get_json()
        long_url = data.get('url', '')
        
        if not long_url:
            return jsonify({'success': False, 'error': 'URL required'})
        
        if not long_url.startswith(('http://', 'https://')):
            long_url = 'https://' + long_url
        
        db = load_db()
        code = generate_code()
        db[code] = long_url
        save_db(db)
        
        base_url = request.host_url.rstrip('/')
        short_url = f"{base_url}/{code}"
        
        return jsonify({'success': True, 'short_url': short_url, 'code': code})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/<code>')
def page1(code):
    db = load_db()
    if code not in db:
        return "Link not found!", 404
    return render_template_string(PAGE1, code=code)

@app.route('/page2/<code>')
def page2_route(code):
    db = load_db()
    if code not in db:
        return "Link not found!", 404
    return render_template_string(PAGE2, code=code)

@app.route('/page3/<code>')
def page3_route(code):
    db = load_db()
    if code not in db:
        return "Link not found!", 404
    return render_template_string(PAGE3, final_url=db[code])

if __name__ == '__main__':
    print("=" * 50)
    print("Short URL Server Started!")
    print("URL: http://localhost:10000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=10000, debug=True)
