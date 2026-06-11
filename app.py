import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

AMAZON_TAG = "midasvip-20"
AWIN_ID = "2930251"

def get_db():
    conn = sqlite3.connect('midasvip_definitivo.db')
    conn.row_factory = sqlite3.Row
    return conn

def gerar_link_afiliado(titulo, categoria):
    termo = titulo.replace(" ", "+")
    cat = (categoria or "").lower()
    if any(t in cat for t in ['beleza', 'perfume', 'cosmetico']):
        return f"https://www.awin1.com/cread.php?awinaffid={AWIN_ID}&p=https%3A%2F%2Fwww.belezanaweb.com.br%2Fbusca%2F%3Fq%3D{termo}"
    return f"https://www.amazon.com.br/s?k={termo}&tag={AMAZON_TAG}&i=fashion"

@app.route('/')
def home():
    conn = get_db()
    noticias = []
    for row in conn.execute('SELECT * FROM noticias ORDER BY id DESC').fetchall():
        n = dict(row)
        n['link_afiliado'] = gerar_link_afiliado(n['titulo'], n.get('categoria', ''))
        noticias.append(n)
    conn.close()
    return render_template('index.html', noticias=noticias)
# (A rota /buscar segue a mesma lógica, aplicando gerar_link_afiliado)