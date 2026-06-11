from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>TESTE MIDASVIP V3</h1>
    <p>Se você está vendo esta mensagem, o deploy novo funcionou.</p>
    """

if __name__ == "__main__":
    app.run()
