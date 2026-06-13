from flask import Flask, render_template
from noticias_manager import carregar_cache
import requests

app = Flask(__name__)

# CONFIGURAÇÕES DA API
API_KEY = "lmd_dev_F8K39DzOwG_Z1pGoeCk7rg1FFouHbuEdXFldOGfsIWc"
SOURCE_ID = "fc89b7ba-30c3-4ff4-ad37-5ebfea125368"

def buscar_produtos_direto(categoria):
    """Busca produtos direto da API sem salvar em arquivo."""
    url = f"https://api.lomadee.com/v3/{API_KEY}/product/_preferred?sourceId={SOURCE_ID}&keyword={categoria}"
    try:
        r = requests.get(url, timeout=5) # Timeout curto para não travar o site
        if r.status_code == 200:
            data = r.json().get('products', [])
            return [{"nome": p['productName'], "descricao": p.get('shortDescription', ''), "link": p['link']} for p in data[:6]]
    except Exception as e:
        print(f"Erro ao buscar {categoria}: {e}")
    return []

# --- ROTAS ---

@app.route("/")
def home():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])

@app.route('/midasvip-select')
def midasvip_select():
    return render_template('midasvip_select.html')

@app.route("/perfumes")
def perfumes():
    return render_template("perfumes.html", produtos=buscar_produtos_direto("perfumes"))

@app.route("/beleza")
def beleza():
    return render_template("beleza.html", produtos=buscar_produtos_direto("beleza"))

@app.route("/moda-feminina")
def moda_feminina():
    return render_template("moda_feminina.html", produtos=buscar_produtos_direto("moda feminina"))

@app.route("/relogios")
def relogios():
    return render_template("relogios.html", produtos=buscar_produtos_direto("relogios"))

@app.route("/bolsas")
def bolsas():
    return render_template("bolsas.html", produtos=buscar_produtos_direto("bolsas"))

@app.route("/moda-masculina")
def moda_masculina():
    return render_template("moda_masculina.html", produtos=buscar_produtos_direto("moda masculina"))

@app.route("/tecnologia")
def tecnologia():
    return render_template("tecnologia.html", produtos=buscar_produtos_direto("tecnologia"))

@app.route("/viagens")
def viagens():
    return render_template("viagens.html", produtos=buscar_produtos_direto("viagens"))

# ROTAS DE NOTÍCIAS E ESTÁTICAS
@app.route("/luxo")
def luxo():
    dados = carregar_cache()
    return render_template("luxo.html", noticias=dados.get("luxo", []), produtos=buscar_produtos_direto("luxo"))

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
