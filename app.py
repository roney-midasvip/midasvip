from flask import Flask, render_template
from noticias_manager import carregar_cache
import json
import os

app = Flask(__name__)

def carregar_produtos():
    """Lê os produtos do arquivo local. Se não achar, retorna vazio."""
    if os.path.exists('produtos_data.json'):
        try:
            with open('produtos_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# 🏠 ROTAS
@app.route("/")
def home():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])

@app.route('/midasvip-select')
def midasvip_select():
    return render_template('midasvip_select.html', produtos=carregar_produtos())

# 🛍️ ROTAS DE PRODUTOS
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

# ROTAS RESTANTES (Notícias, etc)
@app.route("/luxo")
def luxo():
    dados = carregar_cache()
    return render_template("luxo.html", noticias=dados.get("luxo", []), produtos=carregar_produtos().get("luxo", []))

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

@app.route("/quem-somos")
def quem_somos(): return render_template("quem_somos.html")
@app.route("/contato")
def contato(): return render_template("contato.html")
@app.route("/privacidade")
def privacidade(): return render_template("privacidade.html")

if __name__ == "__main__":
    app.run(debug=True)
