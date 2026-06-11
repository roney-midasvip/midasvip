from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/noticias")
def noticias():
    return render_template("noticias.html")

@app.route("/bilionarios")
def bilionarios():
    return render_template("bilionarios.html")

@app.route("/celebridades")
def celebridades():
    return render_template("celebridades.html")

@app.route("/luxo")
def luxo():
    return render_template("luxo.html")

if __name__ == "__main__":
    app.run()
