from flask import Flask, render_template
import requests

app = Flask(__name__)

NEWS_API_KEY = "7a1c6708658f493bb44176f431606bc3"


def buscar_noticias(tema):

    url = (
        "https://newsapi.org/v2/everything?"
        f"q={tema}"
        "&language=en"
        "&sortBy=publishedAt"
        "&pageSize=40"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:

        resposta = requests.get(url, timeout=15)

        if resposta.status_code != 200:
            print("Erro NewsAPI:", resposta.status_code)
            return []

        dados = resposta.json()

        noticias = []
        titulos_vistos = set()

        palavras_bloqueadas = [
            "murder",
            "killed",
            "stabbed",
            "crime",
            "covid",
            "vaccine",
            "war",
            "arrested",
            "soccer odds",
            "betting",
            "recipe",
            "pasta",
            "world cup odds",
            "fugitive"
        ]

        for item in dados.get("articles", []):

            titulo = item.get("title", "")

            if not titulo:
                continue

            titulo_lower = titulo.lower()

            if any(p in titulo_lower for p in palavras_bloqueadas):
                continue

            if titulo in titulos_vistos:
                continue

            titulos_vistos.add(titulo)

            noticias.append({
                "titulo": titulo,
                "link": item.get("url"),
                "imagem": item.get("urlToImage"),
                "fonte": item.get("source", {}).get("name", "Fonte desconhecida"),
                "data": item.get("publishedAt", "")
            })

        return noticias

    except Exception as erro:

        print("ERRO:", erro)
        return []


@app.route("/")
def home():

    noticias = buscar_noticias(
        '"Elon Musk" OR "Jeff Bezos" OR luxury OR celebrity OR billionaire'
    )

    return render_template(
        "index.html",
        noticias=noticias[:8]
    )


@app.route("/noticias")
def noticias():

    noticias = buscar_noticias(
        '"Elon Musk" OR "Jeff Bezos" OR luxury OR celebrity OR billionaire'
    )

    return render_template(
        "noticias.html",
        noticias=noticias
    )


@app.route("/bilionarios")
def bilionarios():

    noticias = buscar_noticias(
        '"Elon Musk" OR "Jeff Bezos" OR "Bernard Arnault" OR "Warren Buffett" OR billionaire OR Forbes'
    )

    return render_template(
        "bilionarios.html",
        noticias=noticias
    )


@app.route("/celebridades")
def celebridades():

    noticias = buscar_noticias(
        '"Taylor Swift" OR "Cristiano Ronaldo" OR "Beyonce" OR celebrity OR Hollywood'
    )

    return render_template(
        "celebridades.html",
        noticias=noticias
    )


@app.route("/luxo")
def luxo():

    noticias = buscar_noticias(
        '"Rolex" OR "Ferrari" OR "Lamborghini" OR "Bugatti" OR "Private Jet" OR "Superyacht"'
    )

    return render_template(
        "luxo.html",
        noticias=noticias
    )

@app.route("/midasvip-select")
def midasvip_select():

    return render_template("midasvip_select.html")

@app.route("/perfumes")
def perfumes():
    return render_template("perfumes.html")


@app.route("/beleza")
def beleza():
    return render_template("beleza.html")


@app.route("/moda-feminina")
def moda_feminina():
    return render_template("moda_feminina.html")


@app.route("/relogios")
def relogios():
    return render_template("relogios.html")


@app.route("/bolsas")
def bolsas():
    return render_template("bolsas.html")


@app.route("/moda-masculina")
def moda_masculina():
    return render_template("moda_masculina.html")


@app.route("/tecnologia")
def tecnologia():
    return render_template("tecnologia.html")


@app.route("/viagens")
def viagens():
    return render_template("viagens.html")
    
if __name__ == "__main__":
    app.run(debug=True)
