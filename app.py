import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

AMAZON_TAG = "midasvip-20"
AWIN_ID = "2930251" # Seu ID está aqui e será usado

def get_db():
    conn = sqlite3.connect('midasvip_definitivo.db')
    conn.row_factory = sqlite3.Row
    return conn

def gerar_link_dinamico(titulo, categoria):
    # Lógica: Se for algo de beleza/estilo, usa Awin. Se não, usa Amazon.
    cat = (categoria or "").lower()
    tit = (titulo or "").lower()
    
    if any(termo in cat or termo in tit for termo in ['beleza', 'perfume', 'cosmetico', 'estilo']):
        # Link Awin com seu ID
        termo_busca = titulo.replace(" ", "+")
        return f"https://www.awin1.com/cread.php?awinaffid={AWIN_ID}&p=https%3A%2F%2Fwww.belezanaweb.com.br%2Fbusca%2F%3Fq%3D{termo_busca}"
    else:
        # Link Amazon com sua Tag
        termo_busca = titulo.replace(" ", "+")
        return f"https://www.amazon.com.br/s?k={termo_busca}&tag={AMAZON_TAG}&i=fashion"

@app.route('/')
def home():
    conn = get_db()
    noticias_raw = conn.execute('SELECT * FROM noticias ORDER BY id DESC').fetchall()
    conn.close()
    
    noticias = []
    for n in noticias_raw:
        item = dict(n)
        item['link_produto'] = gerar_link_dinamico(item['titulo'], item.get('categoria', ''))
        noticias.append(item)
        
    return render_template('index.html', noticias=noticias)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '')
    conn = get_db()
    noticias_raw = conn.execute('SELECT * FROM noticias WHERE titulo LIKE ? OR categoria LIKE ? ORDER BY id DESC', 
                                ('%' + termo + '%', '%' + termo + '%')).fetchall()
    conn.close()
    
    noticias = []
    for n in noticias_raw:
        item = dict(n)
        item['link_produto'] = gerar_link_dinamico(item['titulo'], item.get('categoria', ''))
        noticias.append(item)
        
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True)