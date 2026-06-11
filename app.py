from flask import Flask, render_template
import feedparser

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

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

    feed = feedparser.parse(
        "https://feeds.bbci.co.uk/news/world/rss.xml"
    )

    lista_noticias = []

    for item in feed.entries[:20]:
        lista_noticias.append({
            "titulo": item.title,
            "link": item.link
        })

    return render_template(
        "noticias.html",
        noticias=lista_noticias
    )

if __name__ == "__main__":
    app.run(debug=True)
