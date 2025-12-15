import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


from flask import send_from_directory

@app.route("/app/")
def miniapp():
    return send_from_directory("web", "index.html")

@app.route("/app/<path:path>")
def miniapp_static(path):
    return send_from_directory("web", path)
