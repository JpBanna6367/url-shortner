# app.py - Complete Ad Server with Auto Click

from flask import Flask, request, render_template_string, redirect, jsonify
import random
import string
import json
import os
import time
from datetime import datetime

app = Flask(__name__)

# ======================= CONFIG =======================
DB_FILE = "links.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

def gen_code():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))

# ======================= HTML TEMPLATE =======================
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Link Unlocker - Complete Ad View to Continue</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 100%);
            color: #fff; 
            font-family: 'Segoe UI', Arial, sans-serif; 
            min-height: 100vh;
        }
        
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        
        /* Header */
        .header { 
            background: linear-gradient(135deg, #00ff9d, #00bfff);
            padding: 20px; 
            border-radius: 15px; 
            text-align: center;
            margin-bottom: 20px;
        }
        .header h1 { color: #000; margin-bottom: 5px; }
        .header p { color: #000; opacity: 0.8; }
        
        /* Timer Box */
        .timer-box {
            background: rgba(0,0,0,0.5);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin-bottom: 20px;
            border: 2px solid #00ff9d;
        }
        .timer {
            font-size: 64px;
            font-weight: bold;
            color: #00ff9d;
            font-family: monospace;
        }
        .timer-label {
            font-size: 14px;
            color: #888;
            margin-top: 10px;
        }
        
        /* Ad Banner Section */
        .ad-banner {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .ad-label {
            font-size: 11px;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        /* Scroll Section (hidden initially) */
        .scroll-section {
            max-height: 0;
            overflow: hidden;
            transition: max-height 1s ease-out;
            margin: 20px 0;
        }
        .scroll-section.show {
            max-height: 500px;
        }
        .scroll-content {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .scroll-hint {
            color: #ffcc00;
            animation: bounce 1s infinite;
        }
        
        /* Download Button */
        .download-btn {
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
            transition: transform 0.3s;
        }
        .download-btn:hover {
            transform: scale(1.02);
        }
        .download-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        /* Auto Click Banner (hidden) */
        .auto-click-banner {
            display: none;
        }
        
        /* Info Section */
        .info-section {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            font-size: 12px;
            color: #888;
            text-align: center;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            color: #555;
            font-size: 12px;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 20px;
        }
        .footer a { color: #00bfff; text-decoration: none; }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>🔗 LINK UNLOCKER</h1>
        <p>Complete the steps below to get your link</p>
    </div>
    
    <!-- Timer Box -->
    <div class="timer-box">
        <div class="timer" id="timer">10</div>
        <div class="timer-label">Seconds remaining</div>
    </div>
    
    <!-- Ad Banner 1 - Top -->
    <div class="ad-banner">
        <div class="ad-label">ADVERTISEMENT</div>
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
    
    <!-- Popup Ad Script -->
    <script src="https://pl29414129.profitablecpmratenetwork.com/30/49/df/3049df26bdcf4b8606a8d79ca7b71bde.js"></script>
    
    <!-- Scroll Section (appears after timer) -->
    <div class="scroll-section" id="scrollSection">
        <div class="scroll-content">
            <p class="scroll-hint">👇 <strong>SCROLL DOWN</strong> to continue 👇</p>
            <p style="margin: 10px 0; font-size: 14px;">Continue scrolling to unlock the button</p>
            <div class="progress" style="height: 4px; background: #333; border-radius: 2px; margin: 10px 0;">
                <div id="scrollProgress" style="width: 0%; height: 100%; background: #00ff9d; border-radius: 2px;"></div>
            </div>
        </div>
    </div>
    
    <!-- Ad Banner 2 - Middle -->
    <div class="ad-banner" id="middleAd" style="display: none;">
        <div class="ad-label">SPONSORED</div>
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
    
    <!-- Download Button (disabled initially) -->
    <button class="download-btn" id="downloadBtn" disabled>
        🔥 CLICK HERE TO DOWNLOAD 🔥
    </button>
    <p id="btnMessage" style="text-align: center; font-size: 12px; color: #ff6600; margin-top: 5px;"></p>
    
    <!-- Banner Ad 3 - Bottom -->
    <div class="ad-banner" id="bottomAd">
        <div class="ad-label">ADVERTISEMENT</div>
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
    
    <!-- Hidden Auto-Click Banner -->
    <div class="auto-click-banner">
        <div id="autoClickAd"></div>
    </div>
    
    <div class="info-section">
        ⚡ Complete all steps to unlock your download link
    </div>
    
    <div class="footer">
        Powered by <a href="https://t.me/eaglescrip" target="_blank">@eaglescrip</a>
    </div>
</div>

<script>
    // ======================= CONFIG =======================
    let timeLeft = 10;
    let timerCompleted = false;
    let scrollCompleted = false;
    let adClicked = false;
    let scrollPercent = 0;
    
    // Get elements
    const timerEl = document.getElementById('timer');
    const scrollSection = document.getElementById('scrollSection');
    const middleAd = document.getElementById('middleAd');
    const downloadBtn = document.getElementById('downloadBtn');
    const btnMessage = document.getElementById('btnMessage');
    const scrollProgress = document.getElementById('scrollProgress');
    
    // ======================= TIMER =======================
    const timerInterval = setInterval(function() {
        timeLeft--;
        timerEl.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            timerEl.textContent = "✅ DONE!";
            timerCompleted = true;
            
            // Show scroll section
            setTimeout(() => {
                scrollSection.classList.add('show');
                middleAd.style.display = 'block';
                btnMessage.textContent = "⬇️ Scroll down to continue ⬇️";
            }, 500);
            
            checkAllComplete();
        }
    }, 1000);
    
    // ======================= SCROLL DETECTION =======================
    window.addEventListener('scroll', function() {
        if (!timerCompleted) return;
        
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight;
        const windowHeight = window.innerHeight;
        const maxScroll = scrollHeight - windowHeight;
        
        if (maxScroll > 0) {
            scrollPercent = (scrollTop / maxScroll) * 100;
            scrollProgress.style.width = Math.min(scrollPercent, 100) + '%';
            
            if (scrollPercent >= 80 && !scrollCompleted) {
                scrollCompleted = true;
                scrollProgress.style.width = '100%';
                btnMessage.textContent = "✅ Scroll completed! Now click the button above.";
                checkAllComplete();
            }
        }
    });
    
    // ======================= AUTO CLICK ON BANNER AD =======================
    function autoClickBannerAd() {
        // Find all banner iframes and trigger click
        const iframes = document.querySelectorAll('.ad-banner iframe');
        
        iframes.forEach(iframe => {
            try {
                // Trigger click on iframe content
                const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                if (iframeDoc) {
                    const links = iframeDoc.querySelectorAll('a');
                    links.forEach(link => {
                        link.click();
                    });
                }
            } catch(e) {
                console.log("Cannot access iframe (cross-origin)");
            }
        });
        
        // Alternative: Open popunder
        window.open('https://pl29414129.profitablecpmratenetwork.com/click', '_blank');
    }
    
    // ======================= MAIN BUTTON CLICK =======================
    downloadBtn.addEventListener('click', function() {
        if (!timerCompleted || !scrollCompleted) {
            alert("⚠️ Please complete the timer and scroll down first!");
            return;
        }
        
        if (adClicked) {
            alert("✅ Link already unlocked! Redirecting...");
            window.location.href = "{{ final_url }}";
            return;
        }
        
        adClicked = true;
        btnMessage.innerHTML = "🔄 Processing... Please wait";
        downloadBtn.disabled = true;
        
        // Step 1: Auto click on banner ads
        autoClickBannerAd();
        
        // Step 2: Load popunder ad
        const popunder = window.open('https://pl29414129.profitablecpmratenetwork.com/30/49/df/3049df26bdcf4b8606a8d79ca7b71bde.js', '_blank');
        
        // Step 3: Report click to server
        fetch('/track-click', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: '{{ code }}',
                timestamp: Date.now()
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                btnMessage.innerHTML = "✅ Unlocked! Redirecting...";
                setTimeout(() => {
                    window.location.href = "{{ final_url }}";
                }, 2000);
            } else {
                btnMessage.innerHTML = "❌ Failed! Please try again";
                downloadBtn.disabled = false;
                adClicked = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            btnMessage.innerHTML = "❌ Error! Redirecting anyway...";
            setTimeout(() => {
                window.location.href = "{{ final_url }}";
            }, 3000);
        });
        
        // Fallback: redirect after 10 seconds
        setTimeout(() => {
            if (!adClicked) {
                window.location.href = "{{ final_url }}";
            }
        }, 10000);
    });
    
    function checkAllComplete() {
        if (timerCompleted && scrollCompleted) {
            downloadBtn.disabled = false;
            btnMessage.innerHTML = "✅ Ready! Click the button to get your link";
            btnMessage.style.color = "#00ff9d";
        }
    }
</script>

</body>
</html>
"""

# ======================= FLASK ROUTES =======================
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url', '')
        if original_url:
            db = load_db()
            code = gen_code()
            db[code] = original_url
            save_db(db)
            
            # Render template with code and final URL
            base_url = request.host_url.rstrip('/')
            final_url = f"{base_url}/unlock/{code}"
            
            return render_template_string(
                MAIN_TEMPLATE, 
                code=code, 
                final_url=final_url
            )
    
    # GET request - show create form
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Create Short Link</title>
        <style>
            body {
                background: #0a0a1a;
                color: #fff;
                font-family: Arial;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: #111133;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                width: 90%;
                max-width: 500px;
            }
            input {
                width: 100%;
                padding: 15px;
                margin: 20px 0;
                background: #0a0a1a;
                border: 1px solid #00ff9d;
                border-radius: 10px;
                color: #fff;
                font-size: 16px;
            }
            button {
                background: linear-gradient(135deg, #00ff9d, #00bfff);
                color: #000;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 50px;
                cursor: pointer;
            }
            h1 { color: #00ff9d; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔗 Link Unlocker</h1>
            <p>Paste your long URL below</p>
            <form method="POST">
                <input type="url" name="url" placeholder="https://example.com/your-long-link" required>
                <button type="submit">Create Unlock Link</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/unlock/<code>')
def unlock(code):
    db = load_db()
    original_url = db.get(code)
    if original_url:
        return redirect(original_url)
    return "Link not found!", 404

@app.route('/track-click', methods=['POST'])
def track_click():
    data = request.json
    code = data.get('code')
    
    db = load_db()
    if code in db:
        # Track click in separate file
        import datetime
        stats_file = "clicks.json"
        
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {"total_clicks": 0, "clicks_by_link": {}}
        
        stats["total_clicks"] += 1
        
        if code not in stats["clicks_by_link"]:
            stats["clicks_by_link"][code] = 0
        stats["clicks_by_link"][code] += 1
        
        stats["last_click"] = datetime.datetime.now().isoformat()
        
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=4)
        
        return jsonify({"success": True})
    
    return jsonify({"success": False})

# ======================= RUN SERVER =======================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
