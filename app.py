from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)

RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"


def obter_noticias(limite=5):
    feed = feedparser.parse(RSS_URL)

    noticias = []

    for item in feed.entries[:limite]:
        noticias.append({
            "titulo": item.title,
            "link": item.link
        })

    return noticias


PESSOAS = {
    "elon musk": {
        "nome": "Elon Musk",
        "descricao": "CEO da Tesla, SpaceX e uma das maiores fortunas do mundo."
    },
    "jeff bezos": {
        "nome": "Jeff Bezos",
        "descricao": "Fundador da Amazon e investidor bilionário."
    },
    "mark zuckerberg": {
        "nome": "Mark Zuckerberg",
        "descricao": "Fundador da Meta e um dos empresários mais influentes do planeta."
    },
    "neymar": {
        "nome": "Neymar Jr.",
        "descricao": "Jogador brasileiro e uma das celebridades esportivas mais conhecidas do mundo."
    },
    "cristiano ronaldo": {
        "nome": "Cristiano Ronaldo",
        "descricao": "Atleta global, empresário e ícone do futebol."
    }
}


@app.route("/")
def home():

    noticias = obter_noticias(5)

    return render_template(
        "home.html",
        noticias=noticias
    )


@app.route("/buscar")
def buscar():

    termo = request.args.get("q", "").lower()

    resultado = PESSOAS.get(termo)

    return render_template(
        "buscar.html",
        resultado=resultado,
        termo=termo
    )


@app.route("/bilionarios")
def bilionarios():
    return render_template("bilionarios.html")


@app.route("/celebridades")
def celebridades():
    return render_template("celebridades.html")


@app.route("/luxo")
def luxo():
    return render_template("luxo.html")


@app.route("/noticias")
def noticias():

    lista_noticias = obter_noticias(20)

    return render_template(
        "noticias.html",
        noticias=lista_noticias
    )


if __name__ == "__main__":
    app.run(debug=True)
