from flask import Flask, render_template, send_from_directory
import requests

from cache_noticias import cache_valido, get_cache, atualizar_cache, pode_atualizar

app = Flask(__name__)

NEWS_API_KEY = "7a1c6708658f493bb44176f431606bc3"

# 💰 PRODUTOS POR CATEGORIA (MONETIZAÇÃO)
produtos_por_categoria = {

    "luxo": [
        {
            "nome": "Rolex Submariner",
            "descricao": "Relógio mais icônico do luxo mundial",
            "link": "https://seu-link-afiliado.com"
        },
        {
            "nome": "Ferrari Experience",
            "descricao": "Experiência exclusiva com supercarros",
            "link": "https://seu-link-afiliado.com"
        }
    ],

    "beleza": [
        {
            "nome": "Dior Sauvage",
            "descricao": "Perfume masculino mais vendido do mundo",
            "link": "https://seu-link-afiliado.com"
        },
        {
            "nome": "Chanel No.5",
            "descricao": "Perfume feminino clássico de luxo",
            "link": "https://seu-link-afiliado.com"
        }
    ],

    "moda-masculina": [
        {
            "nome": "Hugo Boss Camisa",
            "descricao": "Elegância masculina premium",
            "link": "https://seu-link-afiliado.com"
        }
    ]
}


# 🧠 NEWS + CACHE
def buscar_noticias(tema):

    if cache_valido():
        return get_cache()

    if not pode_atualizar():
        return get_cache()

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
            return get_cache()

        dados = resposta.json()

        noticias = []
        titulos_vistos = set()

        palavras_bloqueadas = [
            "murder", "killed", "stabbed", "crime", "covid",
            "vaccine", "war", "arrested", "betting", "recipe",
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

        atualizar_cache(noticias)
        return noticias

    except Exception:
        return get_cache()


# 🏠 HOME
@app.route("/")
def home():
    noticias = buscar_noticias("luxury celebrity billionaire")
    return render_template("index.html", noticias=noticias[:8])


# 📰 NOTÍCIAS GERAL
@app.route("/noticias")
def noticias():
    noticias = buscar_noticias("luxury celebrity billionaire")
    return render_template("noticias.html", noticias=noticias)


# 💰 LUXO (MONETIZADO)
@app.route("/luxo")
def luxo():
    noticias = buscar_noticias('"Rolex" OR "Ferrari" OR "Lamborghini" OR "Bugatti" OR "Private Jet"')

    return render_template(
        "luxo.html",
        noticias=noticias,
        produtos=produtos_por_categoria["luxo"]
    )


# 💎 BELEZA (MONETIZADO)
@app.route("/beleza")
def beleza():
    noticias = buscar_noticias('"perfume" OR "beauty" OR "luxury skincare"')

    return render_template(
        "beleza.html",
        noticias=noticias,
        produtos=produtos_por_categoria["beleza"]
    )


# 👔 MODA MASCULINA (MONETIZADO)
@app.route("/moda-masculina")
def moda_masculina():
    noticias = buscar_noticias('"men fashion" OR "luxury clothing"')

    return render_template(
        "moda_masculina.html",
        noticias=noticias,
        produtos=produtos_por_categoria["moda-masculina"]
    )


# 👑 OUTRAS ROTAS (SEM MEXER)
@app.route("/bilionarios")
def bilionarios():
    noticias = buscar_noticias("Elon Musk Jeff Bezos Bernard Arnault Forbes billionaire")
    return render_template("bilionarios.html", noticias=noticias)


@app.route("/celebridades")
def celebridades():
    noticias = buscar_noticias("Taylor Swift Cristiano Ronaldo Beyonce Hollywood celebrity")
    return render_template("celebridades.html", noticias=noticias)


@app.route("/midasvip-select")
def midasvip_select():
    return render_template("midasvip_select.html")


@app.route("/perfumes")
def perfumes():
    return render_template("perfumes.html")


@app.route("/relogios")
def relogios():
    return render_template("relogios.html")


@app.route("/bolsas")
def bolsas():
    return render_template("bolsas.html")


@app.route("/tecnologia")
def tecnologia():
    return render_template("tecnologia.html")


@app.route("/viagens")
def viagens():
    return render_template("viagens.html")


@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')


if __name__ == "__main__":
    app.run(debug=True)
