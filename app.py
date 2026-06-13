from flask import Flask, render_template, send_from_directory
import requests
from cache_noticias import cache_valido, get_cache, atualizar_cache, pode_atualizar

app = Flask(__name__)

NEWS_API_KEY = "7a1c6708658f493bb44176f431606bc3"

# 💰 PRODUTOS POR CATEGORIA
produtos_por_categoria = {
    "luxo": [
        {"nome": "Rolex Submariner", "descricao": "Relógio mais icônico do luxo mundial", "link": "#"},
        {"nome": "Ferrari Experience", "descricao": "Experiência exclusiva com supercarros", "link": "#"}
    ],
    "beleza": [
        {"nome": "Dior Sauvage", "descricao": "Perfume masculino mais vendido do mundo", "link": "#"},
        {"nome": "Chanel No.5", "descricao": "Perfume feminino clássico de luxo", "link": "#"}
    ],
    "moda-masculina": [
        {"nome": "Hugo Boss Camisa", "descricao": "Elegância masculina premium", "link": "#"}
    ]
}

# 🧠 BUSCA CENTRALIZADA (1 CHAMADA)
def buscar_todas_noticias():
    if cache_valido():
        return get_cache()

    if not pode_atualizar():
        return get_cache()

    # Query abrangente para pegar tudo de uma vez
    url = (
        "https://newsapi.org/v2/everything?"
        "q=luxury OR billionaire OR celebrity OR fashion OR watches OR supercars"
        "&language=en"
        "&sortBy=publishedAt"
        "&pageSize=80"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:
        resposta = requests.get(url, timeout=15)
        if resposta.status_code != 200:
            return get_cache()

        dados = resposta.json()
        noticias = []
        titulos_vistos = set()
        palavras_bloqueadas = ["murder", "killed", "stabbed", "crime", "covid", "vaccine", "war", "arrested", "betting", "recipe", "fugitive"]

        for item in dados.get("articles", []):
            titulo = item.get("title")
            if not titulo or any(p in titulo.lower() for p in palavras_bloqueadas) or titulo in titulos_vistos:
                continue

            titulos_vistos.add(titulo)
            noticias.append({
                "titulo": titulo,
                "link": item.get("url"),
                "imagem": item.get("urlToImage"),
                "fonte": item.get("source", {}).get("name", "Fonte desconhecida"),
                "data": item.get("publishedAt", "")
            })

        atualizar_cache(noticias)
        return noticias
    except Exception as e:
        print("ERRO NEWS:", e)
        return get_cache()

# 💡 FILTRO LOCAL (NÃO GASTA API)
def filtrar_por_tema(noticias, keywords):
    return [n for n in noticias if any(k in n['titulo'].lower() for k in keywords)]

# 🏠 ROTAS
@app.route("/")
def home():
    todas = buscar_todas_noticias()
    return render_template("index.html", noticias=todas[:8])

@app.route("/privacidade")
def privacidade():
    return render_template("privacidade.html")

@app.route("/noticias")
def noticias():
    return render_template("noticias.html", noticias=buscar_todas_noticias())

@app.route("/luxo")
def luxo():
    todas = buscar_todas_noticias()
    filtradas = filtrar_por_tema(todas, ["luxury", "rolex", "ferrari", "bugatti", "jet", "yacht", "watch"])
    return render_template("luxo.html", noticias=filtradas, produtos=produtos_por_categoria.get("luxo", []))

@app.route("/bilionarios")
def bilionarios():
    todas = buscar_todas_noticias()
    filtradas = filtrar_por_tema(todas, ["billionaire", "musk", "bezos", "arnault", "forbes", "wealth", "business"])
    return render_template("bilionarios.html", noticias=filtradas)

@app.route("/celebridades")
def celebridades():
    todas = buscar_todas_noticias()
    filtradas = filtrar_por_tema(todas, ["celebrity", "hollywood", "swift", "beyonce", "kardashian", "actor", "singer"])
    return render_template("celebridades.html", noticias=filtradas)

# 👑 OUTRAS ROTAS (Sem notícias dinâmicas)
@app.route("/midasvip-select")
def midasvip_select(): return render_template("midasvip_select.html")

@app.route("/perfumes")
def perfumes(): return render_template("perfumes.html")

@app.route("/relogios")
def relogios(): return render_template("relogios.html")

@app.route("/bolsas")
def bolsas(): return render_template("bolsas.html")

@app.route("/tecnologia")
def tecnologia(): return render_template("tecnologia.html")

@app.route("/viagens")
def viagens(): return render_template("viagens.html")

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

if __name__ == "__main__":
    app.run(debug=True)
