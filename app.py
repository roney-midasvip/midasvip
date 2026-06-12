from flask import Flask, render_template
import requests

app = Flask(__name__)

NEWS_API_KEY = "7a1c6708658f493bb44176f431606bc3"


def buscar_noticias():

    url = (
        "https://newsapi.org/v2/everything?"
        "q=(luxury OR billionaire OR celebrity OR luxury watches OR yachts)"
        "&language=en"
        "&sortBy=publishedAt"
        "&pageSize=12"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:

        resposta = requests.get(url, timeout=10)

        dados = resposta.json()

        noticias = []

        if dados.get("status") == "ok":

            for item in dados.get("articles", []):

                noticias.append({
                    "titulo": item.get("title"),
                    "link": item.get("url")
                })

        return noticias

    except Exception as erro:

        print("ERRO:", erro)

        return []


@app.route("/")
def home():

    noticias = buscar_noticias()

    return render_template(
        "index.html",
        noticias=noticias
    )


@app.route("/noticias")
def noticias():

    noticias = buscar_noticias()

    return render_template(
        "noticias.html",
        noticias=noticias
    )


@app.route("/bilionarios")
def bilionarios():
    return render_template("bilionarios.html")


@app.route("/celebridades")
def celebridades():
    return render_template("celebridades.html")


@app.route("/luxo")
def luxo():
    return render_template("luxo.html")


if __name__ == "__main__":
    app.run()
