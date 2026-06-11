import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Configurações
AMAZON_TAG = "midasvip-20"
AWIN_ID = "2930251"

def obter_conexao_banco():
    conexao = sqlite3.connect('midasvip_definitivo.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def gerar_link(titulo, categoria):
    texto = (titulo + " " + (categoria or "")).lower()
    
    # 1. Se você for aprovado em alguma marca (ex: Beleza na Web), 
    # basta adicionar aqui para o código passar a direcionar para ela.
    if any(termo in texto for termo in ['perfume', 'beleza', 'cosmetico']):
        # Quando aprovado, troque o link abaixo pelo seu link de afiliado da marca
        termo_busca = titulo.replace(" ", "+")
        return f"https://www.awin1.com/cread.php?awinaffid={AWIN_ID}&p=https%3A%2F%2Fwww.belezanaweb.com.br%2Fbusca%2F%3Fq%3D{termo_busca}"
    
    # 2. Lógica para Amazon (Relógios, óculos, luxo)
    # Refinamos para evitar "livros" buscando apenas em departamentos específicos se possível
    else:
        # Usamos termos mais específicos para evitar livros
        # Se for relógio ou óculos, forçamos o termo de busca ser mais preciso
        palavras = titulo.split()[:3]
        termo_busca = "+".join(palavras)
        return f"https://www.amazon.com.br/s?k={termo_busca}&tag={AMAZON_TAG}&i=fashion"

@app.route('/')
def home():
    conexao = obter_conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM noticias ORDER BY id DESC")
    noticias_raw = cursor.fetchall()
    noticias = [dict(n) for n in noticias_raw]
    for n in noticias:
        n['link_produto'] = gerar_link(n['titulo'], n.get('categoria', ''))
    conexao.close()
    return render_template('index.html', noticias=noticias)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '')
    conexao = obter_conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM noticias WHERE titulo LIKE ? OR categoria LIKE ? ORDER BY id DESC", ('%' + termo + '%', '%' + termo + '%'))
    noticias_raw = cursor.fetchall()
    noticias = [dict(n) for n in noticias_raw]
    for n in noticias:
        n['link_produto'] = gerar_link(n['titulo'], n.get('categoria', ''))
    conexao.close()
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)