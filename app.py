from flask import Flask, render_template
import requests

app = Flask(__name__)

# Configurações da API
API_KEY = "lmd_dev_F8K39DzOwG_Z1pGoeCk7rg1FFouHbuEdXFldOGfsIWc"
SOURCE_ID = "fc89b7ba-30c3-4ff4-ad37-5ebfea125368"
# IP da Lomadee para contornar a falha de DNS do servidor
API_IP = "52.67.234.195" 
HEADERS = {"Host": "api.lomadee.com"}

def buscar_produtos_api(categoria):
    """Busca produtos direto na API usando IP fixo para evitar erro de DNS"""
    url = f"https://{API_IP}/v3/{API_KEY}/product/_preferred?sourceId={SOURCE_ID}&keyword={categoria}"
    try:
        # verify=False é usado aqui porque estamos acessando via IP
        response = requests.get(url, headers=HEADERS, timeout=5, verify=False)
        if response.status_code == 200:
            data = response.json()
            return [{"nome": p['productName'], "descricao": p.get('shortDescription', ''), "link": p['link']} 
                    for p in data.get('products', [])[:5]]
    except Exception as e:
        print(f"Erro ao buscar {categoria}: {e}")
    return []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/perfumes")
def perfumes():
    return render_template("perfumes.html", produtos=buscar_produtos_api("perfume"))

@app.route("/beleza")
def beleza():
    return render_template("beleza.html", produtos=buscar_produtos_api("beleza"))

@app.route("/moda-feminina")
def moda_feminina():
    return render_template("moda-feminina.html", produtos=buscar_produtos_api("moda-feminina"))

@app.route("/relogios")
def relogios():
    return render_template("relogios.html", produtos=buscar_produtos_api("relogios"))

@app.route("/bolsas")
def bolsas():
    return render_template("bolsas.html", produtos=buscar_produtos_api("bolsas"))

@app.route("/moda-masculina")
def moda_masculina():
    return render_template("moda-masculina.html", produtos=buscar_produtos_api("moda-masculina"))

@app.route("/tecnologia")
def tecnologia():
    return render_template("tecnologia.html", produtos=buscar_produtos_api("tecnologia"))

@app.route("/viagens")
def viagens():
    return render_template("viagens.html", produtos=buscar_produtos_api("viagens"))

if __name__ == "__main__":
    app.run(debug=True)
