from flask import Flask, render_template
from noticias_manager import carregar_cache
import json
import os

app = Flask(__name__)

# Função auxiliar para carregar os produtos do arquivo JSON gerado pelo robô
def carregar_produtos():
    if os.path.exists('produtos_data.json'):
        with open('produtos_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 🏠 ROTAS PRINCIPAIS
@app.route("/")
def home():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])

@app.route('/midasvip-select')
def midasvip_select():
    produtos = carregar_produtos()
    return render_template('midasvip_select.html', produtos=produtos)

# 🛍️ ROTAS DE PRODUTOS (CATEGORIAS)
@app.route("/perfumes")
def perfumes():
    produtos = carregar_produtos()
    return render_template("perfumes.html", produtos=produtos.get("perfumes", []))

@app.route("/beleza")
def beleza():
    produtos = carregar_produtos()
    return render_template("beleza.html", produtos=produtos.get("beleza", []))

@app.route("/moda-feminina")
def moda_feminina():
    produtos = carregar_produtos()
    return render_template("moda_feminina.html", produtos=produtos.get("moda-feminina", []))

@app.route("/relogios")
def relogios():
    produtos = carregar_produtos()
    return render_template("relogios.html", produtos=produtos.get("relogios", []))

@app.route("/bolsas")
def bolsas():
    produtos = carregar_produtos()
    return render_template("bolsas.html", produtos=produtos.get("bolsas", []))

@app.route("/moda-masculina")
def moda_masculina():
    produtos = carregar_produtos()
    return render_template("moda_masculina.html", produtos=produtos.get("moda-masculina", []))

@app.route("/tecnologia")
def tecnologia():
    produtos = carregar_produtos()
    return render_template("tecnologia.html", produtos=produtos.get("tecnologia", []))

@app.route("/viagens")
def viagens():
    produtos = carregar_produtos()
    return render_template("viagens.html", produtos=produtos.get("viagens", []))

# 📰 ROTAS DE NOTÍCIAS
@app.route("/luxo")
def luxo():
    dados = carregar_cache()
    produtos = carregar_produtos()
    return render_template("luxo.html", noticias=dados.get("luxo", []), produtos=produtos.get("luxo", []))

@app.route("/bilionarios")
def bilionarios():
    dados = carregar_cache()
    return render_template("bilionarios.html", noticias=dados.get("bilionarios", []))

@app.route("/celebridades")
def celebridades():
    dados = carregar_cache()
    return render_template("celebridades.html", noticias=dados.get("celebridades", []))

@app.route("/noticias")
def noticias(): 
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("noticias.html", noticias=todas)

# 📄 ROTAS ESTÁTICAS
@app.route("/quem-somos")
def quem_somos(): return render_template("quem_somos.html")
@app.route("/contato")
def contato(): return render_template("contato.html")
@app.route("/privacidade")
def privacidade(): return render_template("privacidade.html")

if __name__ == "__main__":
    app.run(debug=True)
