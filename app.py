import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open('noticias.json', 'r', encoding='utf-8') as f:
            artigos = json.load(f)
    except:
        artigos = []
    return render_template("index.html", resultados=artigos)

if __name__ == "__main__":
    app.run()
