from flask import Flask, render_template
import requests

app = Flask(__name__)

NEWS_API_KEY = "7a1c6708658f493bb44176f431606bc3"


def buscar_noticias():

    url = (
        "https://newsapi.org/v2/everything?"
        'q=("luxury" OR "billionaire" OR "celebrity" OR "forbes" OR "richest" OR "superyacht" OR "luxury watch")'
        "&language=en"
        "&sortBy=publishedAt"
        "&pageSize=20"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:

        resposta = requests.get(url, timeout=15)

        if resposta.status_code != 200:
            print("Erro API:", resposta.status_code)
            return []

        dados = resposta.json()

        noticias = []
        titulos_vistos = set()

        for item in dados.get("articles", []):

            titulo = item.get("title")

            if not titulo:
                continue

            if titulo in titulos_vistos:
                continue

            titulos_vistos.add(titulo)

            noticias.append({
                "titulo": titulo,
                "link": item.get("url"),
                "imagem": item.get("urlToImage"),
                "fonte": item.get("source", {}).get("name", "Fonte desconhecida")
            })

        return noticias

    except Exception as erro:

        print("ERRO NEWSAPI:", erro)

        return []


@app.route("/")
def home():

    noticias = buscar_noticias()

    return render_template(
        "home.html",
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
    app.run(debug=True)
