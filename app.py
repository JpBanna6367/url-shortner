# shorturl_server.py - Short URL Generator with Copy Button

from flask import Flask, request, render_template_string, redirect
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

# ======================= MAIN PAGE - Create Short URL =======================
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
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .sub {
            color: #666;
            margin-bottom: 30px;
        }
        input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
            transition: 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            transition: 0.3s;
        }
        button:hover {
            transform: scale(1.02);
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
            margin-top: 0;
        }
        .copy-btn:hover {
            background: #218838;
        }
        .info {
            font-size: 12px;
            color: #888;
            margin-top: 15px;
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Short URL Generator</h1>
        <p class="sub">Paste your long URL and get a short link</p>
        
        <form id="urlForm">
            <input type="url" id="longUrl" placeholder="https://example.com/your-very-long-url" required>
            <button type="submit">✨ Generate Short URL</button>
        </form>
        
        <div class="result-box" id="resultBox">
            <p style="margin-bottom: 10px;">✅ Your Short URL:</p>
            <div class="short-url" id="shortUrl"></div>
            <button class="copy-btn" onclick="copyToClipboard()">📋 Copy to Clipboard</button>
            <p class="info">⚠️ Copy this link and open in browser to visit the destination</p>
        </div>
        
        <div class="footer">
            Powered by ShortURL
        </div>
    </div>
    
    <script>
        const form = document.getElementById('urlForm');
        const longUrlInput = document.getElementById('longUrl');
        const resultBox = document.getElementById('resultBox');
        const shortUrlSpan = document.getElementById('shortUrl');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const longUrl = longUrlInput.value.trim();
            if (!longUrl) {
                alert('Please enter a URL');
                return;
            }
            
            const response = await fetch('/api/shorten', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: longUrl })
            });
            
            const data = await response.json();
            
            if (data.success) {
                shortUrlSpan.textContent = data.short_url;
                resultBox.style.display = 'block';
                longUrlInput.value = '';
            } else {
                alert('Error: ' + data.error);
            }
        });
        
        function copyToClipboard() {
            const url = shortUrlSpan.textContent;
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

# ======================= AD PAGE (When user opens short URL) =======================
AD_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Please Wait</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 100%);
            font-family: 'Segoe UI', Arial, sans-serif;
            min-height: 100vh;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        
        /* Timer Box */
        .timer-box {
            background: rgba(0,0,0,0.5);
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            border: 2px solid #00ff9d;
        }
        .timer {
            font-size: 80px;
            font-weight: bold;
            color: #00ff9d;
            font-family: monospace;
        }
        
        /* Large Banner */
        .large-banner {
            background: #111133;
            border-radius: 15px;
            padding: 10px;
            margin: 20px 0;
            text-align: center;
            border: 1px solid #00ff9d33;
        }
        .small-banner {
            background: #111133;
            border-radius: 10px;
            padding: 8px;
            margin: 10px 0;
            text-align: center;
            border: 1px solid #ff660033;
        }
        .banner-label {
            font-size: 10px;
            color: #666;
            margin-bottom: 5px;
        }
        
        /* Next Button */
        .next-btn {
            background: linear-gradient(135deg, #00ff9d, #00bfff);
            color: #000;
            border: none;
            padding: 18px 40px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            width: 100%;
            margin: 20px 0;
            display: none;
        }
        .next-btn:hover {
            transform: scale(1.02);
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #555;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Timer -->
        <div class="timer-box">
            <div class="timer" id="timer">10</div>
        </div>
        
        <!-- Large Banner 728x90 -->
        <div class="large-banner">
            <div class="banner-label">ADVERTISEMENT</div>
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
        
        <!-- Small Banner 320x50 -->
        <div class="small-banner">
            <div class="banner-label">SPONSORED</div>
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
        
        <!-- Next Button -->
        <button class="next-btn" id="nextBtn" onclick="goToNext()">➡️ NEXT PAGE</button>
        
        <div class="footer">Please wait {{ seconds }} seconds to continue</div>
    </div>
    
    <script>
        let timeLeft = {{ seconds }};
        const timerEl = document.getElementById('timer');
        const nextBtn = document.getElementById('nextBtn');
        
        const timerInterval = setInterval(function() {
            timeLeft--;
            timerEl.textContent = timeLeft;
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                timerEl.textContent = "✅ READY";
                nextBtn.style.display = 'block';
            }
        }, 1000);
        
        function goToNext() {
            window.location.href = '/page2/{{ code }}';
        }
    </script>
</body>
</html>
"""

# ======================= FLASK ROUTES =======================
@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/api/shorten', methods=['POST'])
def api_shorten():
    data = request.json
    long_url = data.get('url', '')
    
    if not long_url:
        return jsonify({'success': False, 'error': 'URL required'})
    
    if not long_url.startswith('http'):
        long_url = 'https://' + long_url
    
    db = load_db()
    code = generate_code()
    db[code] = long_url
    save_db(db)
    
    base_url = request.host_url.rstrip('/')
    short_url = f"{base_url}/{code}"
    
    return jsonify({'success': True, 'short_url': short_url, 'code': code})

@app.route('/<code>')
def ad_page(code):
    db = load_db()
    if code not in db:
        return "Link not found!", 404
    
    # Store in session or pass as param
    return render_template_string(AD_PAGE, code=code, seconds=10)

# Store original URL for redirect (simplified - use session in production)
url_cache = {}

@app.route('/page2/<code>')
def page2(code):
    db = load_db()
    if code not in db:
        return "Link not found!", 404
    
    # Store for final redirect
    url_cache[code] = db[code]
    
    # Page 2 same as Page 1 but different timer
    PAGE2 = AD_PAGE.replace("NEXT PAGE", "NEXT PAGE (2/3)").replace("{{ seconds }}", "8").replace("/page2/", "/page3/")
    return render_template_string(PAGE2, code=code, seconds=8)

@app.route('/page3/<code>')
def page3(code):
    db = load_db()
    if code not in db:
        return "Link not found!", 404
    
    PAGE3 = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Get Your Link</title>
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
            .warning {
                color: #ff6600;
                font-size: 12px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Your Link is Ready!</h1>
            <button class="get-link-btn" onclick="getLink()">🔗 GET LINK</button>
            <button class="support-btn" onclick="supportClick()">💪 SUPPORT US (Click to close ad)</button>
            <p class="warning">⚠️ Click "GET LINK" to proceed</p>
        </div>
        
        <script>
            let popunderOpened = false;
            
            function getLink() {
                if (!popunderOpened) {
                    // Open popunder ad
                    window.open('https://pl29414129.profitablecpmratenetwork.com/click', '_blank');
                    popunderOpened = true;
                    setTimeout(() => {
                        window.location.href = "{{ final_url }}";
                    }, 1000);
                } else {
                    window.location.href = "{{ final_url }}";
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
    final_url = db[code]
    return render_template_string(PAGE3, final_url=final_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
