from flask import Flask, render_template
from noticias_manager import carregar_cache

app = Flask(__name__)

# =========================
# HOME
# =========================

@app.route("/")
def home():
    dados = carregar_cache()

    todas = (
        dados.get("bilionarios", [])
        + dados.get("celebridades", [])
        + dados.get("luxo", [])
    )

    return render_template(
        "index.html",
        noticias=todas[:8]
    )

# =========================
# NOTÍCIAS
# =========================

@app.route("/noticias")
def noticias():
    dados = carregar_cache()

    todas = (
        dados.get("bilionarios", [])
        + dados.get("celebridades", [])
        + dados.get("luxo", [])
    )

    return render_template(
        "noticias.html",
        noticias=todas
    )

# =========================
# CELEBRIDADES
# =========================

@app.route("/celebridades")
def celebridades():
    dados = carregar_cache()

    return render_template(
        "celebridades.html",
        noticias=dados.get("celebridades", [])
    )

# =========================
# BILIONÁRIOS
# =========================

@app.route("/bilionarios")
def bilionarios():
    dados = carregar_cache()

    return render_template(
        "bilionarios.html",
        noticias=dados.get("bilionarios", [])
    )

# =========================
# LUXO
# =========================

@app.route("/luxo")
def luxo():
    dados = carregar_cache()

    return render_template(
        "luxo.html",
        noticias=dados.get("luxo", [])
    )

# =========================
# UNIVERSO MIDASVIP
# =========================

@app.route("/midasvip-select")
def midasvip_select():
    return render_template("midasvip_select.html")

# =========================
# CATEGORIAS
# =========================

@app.route("/perfumes")
def perfumes():
    return render_template("perfumes.html")

@app.route("/beleza")
def beleza():
    return render_template("beleza.html")

@app.route("/moda-feminina")
def moda_feminina():
    return render_template("moda_feminina.html")

@app.route("/moda-masculina")
def moda_masculina():
    return render_template("moda_masculina.html")

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

# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)
