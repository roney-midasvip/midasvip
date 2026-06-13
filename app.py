from flask import Flask, render_template
from noticias_manager import carregar_cache # Nova importação correta

app = Flask(__name__)

# 💰 PRODUTOS POR CATEGORIA
produtos_por_categoria = {
    "luxo": [
        {"nome": "Rolex Submariner", "descricao": "Relógio mais icônico do luxo mundial", "link": "#"},
        {"nome": "Ferrari Experience", "descricao": "Experiência exclusiva com supercarros", "link": "#"}
    ]
}

# 🏠 ROTAS
@app.route("/")
def home():
    dados = carregar_cache()
    # Pega uma mistura de todas as categorias para a home
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])

@app.route("/luxo")
def luxo():
    dados = carregar_cache()
    return render_template("luxo.html", noticias=dados.get("luxo", []), produtos=produtos_por_categoria.get("luxo", []))

@app.route("/bilionarios")
def bilionarios():
    dados = carregar_cache()
    return render_template("bilionarios.html", noticias=dados.get("bilionarios", []))

@app.route("/celebridades")
def celebridades():
    dados = carregar_cache()
    return render_template("celebridades.html", noticias=dados.get("celebridades", []))

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
