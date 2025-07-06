from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080, debug=False)

def keep_alive():
    """Start the Flask webserver in a separate thread"""
    t = Thread(target=run, daemon=True)
    t.start()
    print("🌐 Webserver started on http://0.0.0.0:8080")