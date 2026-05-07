from flask import Flask, request, redirect, jsonify
import random, string, json, os

app = Flask(__name__)
DB_FILE = "urls.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, 'w') as f: json.dump(db, f)

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.json.get('url', '')
    if not url: return jsonify({"error": "URL required"}), 400
    db = load_db()
    code = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))
    db[code] = url
    save_db(db)
    base = request.host_url
    return jsonify({"short_url": f"{base}{code}", "code": code})

@app.route('/<code>')
def go(code):
    db = load_db()
    url = db.get(code)
    if url: return redirect(url, 302)
    return "Not found!", 404

@app.route('/')
def home():
    return "URL Shortener API Ready!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
