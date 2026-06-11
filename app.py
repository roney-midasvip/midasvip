from flask import Flask, render_template
import feedparser

app = Flask(__name__)

RSS_URL = "https://feeds.bbci.co.uk/news/business/rss.xml"

@app.route("/")
def home():
    feed = feedparser.parse(RSS_URL)

    noticias = []

    for item in feed.entries[:12]:
        noticias.append({
            "titulo": item.title,
            "link": item.link
        })

    return render_template(
        "index.html",
        noticias=noticias
    )

if __name__ == "__main__":
    app.run(debug=True)
