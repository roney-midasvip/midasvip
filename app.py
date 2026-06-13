from flask import Flask, render_template
from noticias_manager import carregar_cache
import json
import os

app = Flask(__name__)

# Função para carregar os produtos gerados pelo robô
def carregar_produtos():
    if os.path.exists('produtos_data.json'):
        with open('produtos_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 🏠 ROTAS
@app.route("/")
def home():
    dados = carregar_cache()
    # Pega uma mistura de todas as categorias para a home
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])

@app.route('/midasvip-select')
def midasvip_select():
    # Passamos os produtos para a página de seleção
    produtos = carregar_produtos()
    return render_template('midasvip_select.html', produtos=produtos)

@app.route("/luxo")
def luxo():
    dados = carregar_cache()
    produtos = carregar_produtos()
    return render_template("luxo.html", 
                           noticias=dados.get("luxo", []), 
                           produtos=produtos.get("luxo", []))

@app.route("/bilionarios")
def bilionarios():
    dados = carregar_cache()
    return render_template("bilionarios.html", noticias=dados.get("bilionarios", []))

@app.route("/celebridades")
def celebridades():
    dados = carregar_cache()
    return render_template("celebridades.html", noticias=dados.get("celebridades", []))

# Rotas de categorias (Exemplo para perfumes, basta repetir o padrão para as outras)
@app.route("/perfumes")
def perfumes():
    produtos = carregar_produtos()
    return render_template("perfumes.html", produtos=produtos.get("perfumes", []))

# Rotas estáticas
@app.route("/quem-somos")
def quem_somos(): return render_template("quem_somos.html")
@app.route("/contato")
def contato(): return render_template("contato.html")
@app.route("/privacidade")
def privacidade(): return render_template("privacidade.html")
@app.route("/noticias")
def noticias(): 
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("noticias.html", noticias=todas)

if __name__ == "__main__":
    app.run(debug=True)
