import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Configurações iniciais
AMAZON_TAG = "midasvip-20"
AWIN_ID = "2930251"

def get_db():
    conn = sqlite3.connect('midasvip_definitivo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db()
    # Pega todas as notícias
    noticias = conn.execute('SELECT * FROM noticias ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', noticias=noticias)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '')
    conn = get_db()
    # Busca com LIKE, se não achar nada, ele retorna lista vazia
    query = 'SELECT * FROM noticias WHERE titulo LIKE ? OR categoria LIKE ? ORDER BY id DESC'
    noticias = conn.execute(query, ('%' + termo + '%', '%' + termo + '%')).fetchall()
    conn.close()
    
    # Se a busca não retornar nada, recarrega a home para não ficar vazio
    if not noticias:
        return home()
        
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True)