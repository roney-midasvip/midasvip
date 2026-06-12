from flask import Flask, render_template
import requests

app = Flask(**name**)

NEWS_API_KEY = "7a1c6708658f493bb44176f431606bc3"

def buscar_noticias(tema):

```
url = (
    "https://newsapi.org/v2/everything?"
    f"q={tema}"
    "&language=en"
    "&sortBy=publishedAt"
    "&pageSize=40"
    f"&apiKey={NEWS_API_KEY}"
)

try:

    resposta = requests.get(url, timeout=15)

    if resposta.status_code != 200:
        print("Erro NewsAPI:", resposta.status_code)
        return []

    dados = resposta.json()

    noticias = []
    titulos_vistos = set()

    palavras_bloqueadas = [

        "murder",
        "killed",
        "stabbed",
        "crime",
        "criminal",
        "arrested",
        "arrest",
        "prison",
        "jail",
        "court",

        "war",
        "military",
        "missile",
        "terror",
        "terrorist",

        "election",
        "president",
        "government",
        "minister",
        "senate",
        "congress",
        "politics",

        "covid",
        "vaccine",
        "hospital",
        "disease",
        "virus",

        "earthquake",
        "flood",
        "hurricane",
        "storm",

        "world cup odds",
        "betting",
        "sports betting",

        "recipe",
        "teacher",
        "school",
        "student"
    ]

    for item in dados.get("articles", []):

        titulo = item.get("title", "")

        if not titulo:
            continue

        titulo_lower = titulo.lower()

        if any(p in titulo_lower for p in palavras_bloqueadas):
            continue

        if titulo in titulos_vistos:
            continue

        titulos_vistos.add(titulo)

        noticias.append({
            "titulo": titulo,
            "link": item.get("url"),
            "imagem": item.get("urlToImage"),
            "fonte": item.get("source", {}).get("name", "Fonte desconhecida"),
            "data": item.get("publishedAt", "")
        })

    return noticias

except Exception as erro:

    print("ERRO:", erro)
    return []
```

@app.route("/")
def home():

```
noticias = buscar_noticias(
    '"Elon Musk" OR billionaire OR celebrity OR luxury'
)

return render_template(
    "index.html",
    noticias=noticias[:8]
)
```

@app.route("/noticias")
def noticias():

```
noticias = buscar_noticias(
    '"Elon Musk" OR billionaire OR celebrity OR luxury'
)

return render_template(
    "noticias.html",
    noticias=noticias
)
```

@app.route("/bilionarios")
def bilionarios():

```
noticias = buscar_noticias(
    'billionaire OR wealth OR fortune OR Forbes OR entrepreneur'
)

return render_template(
    "bilionarios.html",
    noticias=noticias
)
```

@app.route("/celebridades")
def celebridades():

```
noticias = buscar_noticias(
    'celebrity OR actor OR actress OR singer OR Hollywood'
)

return render_template(
    "celebridades.html",
    noticias=noticias
)
```

@app.route("/luxo")
def luxo():

```
noticias = buscar_noticias(
    '"luxury brand" OR '
    '"luxury watch" OR '
    '"rolex" OR '
    '"patek philippe" OR '
    '"richard mille" OR '
    '"ferrari" OR '
    '"lamborghini" OR '
    '"bugatti" OR '
    '"rolls-royce" OR '
    '"bentley" OR '
    '"superyacht" OR '
    '"megayacht" OR '
    '"private jet"'
)

return render_template(
    "luxo.html",
    noticias=noticias
)
```

if **name** == "**main**":
app.run(debug=True)
