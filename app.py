from flask import Flask, render_template
from noticias_manager import carregar_cache
import json
import os
import requests

app = Flask(__name__)

# CONFIGURAÇÕES DA API
API_KEY = "lmd_dev_F8K39DzOwG_Z1pGoeCk7rg1FFouHbuEdXFldOGfsIWc"
SOURCE_ID = "fc89b7ba-30c3-4ff4-ad37-5ebfea125368"

def atualizar_produtos_automaticamente():

def carregar_produtos():
    atualizar_produtos_automaticamente()
    if os.path.exists('produtos_data.json'):
        with open('produtos_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# --- ROTAS COMPLETAS ---

@app.route("/")
def home():
    dados = carregar_cache()
    # Soma as categorias que existem no seu manager
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])

@app.route("/noticias")
def noticias():
    # Agrupa tudo para a página de notícias, já que seu manager não tem chave 'noticias'
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

@app.route('/midasvip-select')
def midasvip_select():
    produtos = carregar_produtos()
    return render_template('midasvip_select.html', produtos=produtos)

@app.route("/perfumes")
def perfumes():
    return render_template("perfumes.html", produtos=carregar_produtos().get("perfumes", []))

@app.route("/beleza")
def beleza():
    return render_template("beleza.html", produtos=carregar_produtos().get("beleza", []))

@app.route("/moda-feminina")
def moda_feminina():
    return render_template("moda_feminina.html", produtos=carregar_produtos().get("moda-feminina", []))

@app.route("/relogios")
def relogios():
    return render_template("relogios.html", produtos=carregar_produtos().get("relogios", []))

@app.route("/bolsas")
def bolsas():
    return render_template("bolsas.html", produtos=carregar_produtos().get("bolsas", []))

@app.route("/moda-masculina")
def moda_masculina():
    return render_template("moda_masculina.html", produtos=carregar_produtos().get("moda-masculina", []))

@app.route("/tecnologia")
def tecnologia():
    return render_template("tecnologia.html", produtos=carregar_produtos().get("tecnologia", []))

@app.route("/viagens")
def viagens():
    return render_template("viagens.html", produtos=carregar_produtos().get("viagens", []))

if __name__ == "__main__":
    app.run(debug=True)
