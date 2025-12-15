from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/app/")
def miniapp():
    return send_from_directory("web", "index.html")

@app.route("/app/<path:path>")
def miniapp_static(path):
    return send_from_directory("web", path)
