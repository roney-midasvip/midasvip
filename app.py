from flask import Flask, render_template
from noticias_manager import carregar_cache
import json
import os
import requests

app = Flask(__name__)

# CONFIGURAÇÕES DA API
API_KEY = "SUA_API_KEY_AQUI" # MANTENHA A SUA AQUI
SOURCE_ID = "fc89b7ba-30c3-4ff4-ad37-5ebfea125368"

def atualizar_produtos_automaticamente():
    """Busca produtos da API caso o arquivo ainda não exista."""
    if os.path.exists('produtos_data.json'):
        return # Já existe, não precisa buscar de novo agora
    
    print("--- Buscando produtos automaticamente... ---")
    categorias = ["perfumes", "beleza", "moda-feminina", "relogios", "bolsas", "moda-masculina", "tecnologia", "viagens"]
    base_produtos = {}

    for cat in categorias:
        url = f"https://api.lomadee.com/v3/{API_KEY}/product/_preferred?sourceId={SOURCE_ID}&keyword={cat}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                base_produtos[cat] = [{"nome": p['productName'], "descricao": p.get('shortDescription', ''), "link": p['link']} 
                                      for p in r.json().get('products', [])[:5]]
        except: pass
    
    with open('produtos_data.json', 'w', encoding='utf-8') as f:
        json.dump(base_produtos, f, ensure_ascii=False, indent=4)

def carregar_produtos():
    atualizar_produtos_automaticamente() # Garante que exista
    if os.path.exists('produtos_data.json'):
        with open('produtos_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# --- ROTAS ---
# (Suas rotas permanecem IGUAIS ao que você me passou, 
#  o carregar_produtos() agora se encarrega de tudo!)

@app.route("/")
def home():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])

@app.route('/midasvip-select')
def midasvip_select():
    produtos = carregar_produtos()
    return render_template('midasvip_select.html', produtos=produtos)

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

# ... (Mantenha as outras rotas de notícias e estáticas como estavam)

if __name__ == "__main__":
    app.run(debug=True)
