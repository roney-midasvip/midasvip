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
    ]
}

# 🧠 BUSCA CENTRALIZADA (1 CHAMADA)
def buscar_todas_noticias():
    if cache_valido():
        return get_cache()

    if not pode_atualizar():
        return get_cache()

    # Query restritiva: busca termos de luxo e exclui ativamente termos negativos
    url = (
        "https://newsapi.org/v2/everything?"
        "q=(luxo OR bilionario OR celebridade OR lifestyle OR supercarro OR relogio)"
        "&language=pt"
        "&sortBy=relevancy"
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
        
        # Filtros de segurança mais agressivos
        palavras_bloqueadas = [
            "assassinato", "morto", "esfaqueado", "crime", "covid", "vacina", 
            "guerra", "preso", "aposta", "receita", "fugitivo", "nua", "agredido",
            "trisal", "erotico", "policia", "homicidio"
        ]
        
        fontes_bloqueadas = ["Blog.br", "Fonte Desconhecida", "Msn.com"]

        for item in dados.get("articles", []):
            titulo = item.get("title", "")
            fonte = item.get("source", {}).get("name", "")
            
            # Verificação de qualidade e segurança
            if not titulo or any(p in titulo.lower() for p in palavras_bloqueadas) or fonte in fontes_bloqueadas or titulo in titulos_vistos:
                continue

            titulos_vistos.add(titulo)
            noticias.append({
                "titulo": titulo,
                "link": item.get("url"),
                "imagem": item.get("urlToImage"),
                "fonte": fonte,
                "data": item.get("publishedAt", "")
            })

        atualizar_cache(noticias)
        return noticias
    except Exception as e:
        print("ERRO NEWS:", e)
        return get_cache()

# 💡 FILTRO LOCAL
def filtrar_por_tema(noticias, keywords):
    return [n for n in noticias if any(k in n['titulo'].lower() for k in keywords)]

# 🏠 ROTAS
@app.route("/")
def home():
    todas = buscar_todas_noticias()
    return render_template("index.html", noticias=todas[:8])

@app.route("/luxo")
def luxo():
    todas = buscar_todas_noticias()
    filtradas = filtrar_por_tema(todas, ["luxo", "rolex", "ferrari", "bugatti", "jato", "iate", "relogio", "premium"])
    return render_template("luxo.html", noticias=filtradas, produtos=produtos_por_categoria.get("luxo", []))

@app.route("/bilionarios")
def bilionarios():
    todas = buscar_todas_noticias()
    filtradas = filtrar_por_tema(todas, ["bilionario", "musk", "bezos", "arnault", "forbes", "riqueza", "negocios", "fortuna"])
    return render_template("bilionarios.html", noticias=filtradas)

@app.route("/celebridades")
def celebridades():
    todas = buscar_todas_noticias()
    filtradas = filtrar_por_tema(todas, ["celebridade", "hollywood", "famosos", "ator", "cantor", "lifestyle"])
    return render_template("celebridades.html", noticias=filtradas)

# Rotas estáticas
@app.route("/quem-somos")
def quem_somos(): return render_template("quem_somos.html")
@app.route("/contato")
def contato(): return render_template("contato.html")
@app.route("/privacidade")
def privacidade(): return render_template("privacidade.html")
@app.route("/noticias")
def noticias(): return render_template("noticias.html", noticias=buscar_todas_noticias())

if __name__ == "__main__":
    app.run(debug=True)
