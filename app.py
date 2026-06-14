from flask import Flask, render_template
from noticias_manager import carregar_cache
import requests

app = Flask(__name__)

API_KEY = "lmd_dev_F8K39DzOwG_Z1pGoeCk7rg1FFouHbuEdXFldOGfsIWc"
API_URL = "https://api-beta.lomadee.com.br/affiliate/products"


def buscar_produtos(search, limite=24, preco_min=400):
    try:
        headers = {
            "x-api-key": API_KEY
        }

        params = {
            "page": 1,
            "limit": limite,
            "search": search,
            "price": f"{preco_min * 100}:99999999",
            "isAvailable": "true"
        }

        r = requests.get(API_URL, headers=headers, params=params, timeout=20)

        if r.status_code != 200:
            print("Erro LinkMyDeals:", r.status_code, r.text[:500])
            return []

        dados = r.json()
        return dados.get("data", [])

    except Exception as e:
        print("Erro ao buscar produtos:", e)
        return []


@app.route("/")
def home():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])


@app.route("/noticias")
def noticias():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("noticias.html", noticias=todas)


@app.route("/celebridades")
def celebridades():
    dados = carregar_cache()
    return render_template("celebridades.html", noticias=dados.get("celebridades", []))


@app.route("/bilionarios")
def bilionarios():
    dados = carregar_cache()
    return render_template("bilionarios.html", noticias=dados.get("bilionarios", []))


@app.route("/luxo")
def luxo():
    dados = carregar_cache()
    return render_template("luxo.html", noticias=dados.get("luxo", []))


@app.route("/midasvip-select")
def midasvip_select():
    return render_template("midasvip_select.html")


@app.route("/perfumes")
def perfumes():
    produtos = buscar_produtos("perfume", 24, 400)
    return render_template("perfumes.html", produtos=produtos)


@app.route("/beleza")
def beleza():
    produtos = buscar_produtos("creme", 24, 200)
    return render_template("beleza.html", produtos=produtos)


@app.route("/moda-feminina")
def moda_feminina():
    produtos = buscar_produtos("bolsa", 24, 300)
    return render_template("moda_feminina.html", produtos=produtos)


@app.route("/relogios")
def relogios():
    produtos = buscar_produtos("relógio", 24, 300)
    if not produtos:
        produtos = buscar_produtos("relogio", 24, 300)
    return render_template("relogios.html", produtos=produtos)


@app.route("/bolsas")
def bolsas():
    produtos = buscar_produtos("bolsa", 24, 300)
    return render_template("bolsas.html", produtos=produtos)


@app.route("/moda-masculina")
def moda_masculina():
    produtos = buscar_produtos("tenis", 24, 300)
    return render_template("moda_masculina.html", produtos=produtos)


@app.route("/tecnologia")
def tecnologia():
    produtos = buscar_produtos("smartphone", 24, 400)
    if not produtos:
        produtos = buscar_produtos("fone", 24, 300)
    return render_template("tecnologia.html", produtos=produtos)


@app.route("/viagens")
def viagens():
    produtos = buscar_produtos("mala", 24, 300)
    return render_template("viagens.html", produtos=produtos)


if __name__ == "__main__":
    app.run(debug=True)
