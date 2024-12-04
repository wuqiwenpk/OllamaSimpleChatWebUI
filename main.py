import json

import requests
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return redirect('https://ollama.com/public/icon-32x32.png')


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/model", methods=["POST"])
def model():
    models = []
    api_url = request.json.get("url")
    try:
        response = requests.get(f"{api_url}/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get("models")
            models = [m["name"] for m in models]
    except:
        pass

    return jsonify({"models": models})


@app.route("/chat", methods=["POST"])
def chat():
    ask = request.json.get("ask")
    model_name = request.json.get("model")
    url = request.json.get("url")
    url = f"{url}/api/chat"
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": ask}],
        "stream": True
    }
    response = requests.post(url, json=payload)
    messages = []
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                messages.append(json.loads(line)["message"]["content"])

    return jsonify({"messages": messages})


if __name__ == '__main__':
    app.run(debug=True)
