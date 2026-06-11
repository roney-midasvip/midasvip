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
    # Unificamos o texto para checagem (titulo + categoria)
    texto_para_analise = (titulo + " " + (categoria if categoria else "")).lower()
    
    # Lista expandida para garantir que itens de luxo vão para a Awin
    termos_beleza_luxo = [
        'beleza', 'perfume', 'maquiagem', 'batom', 'skincare', 'sephora', 
        'creme', 'cosmético', 'cabelo', 'luxo', 'fashion', 'estilo', 'joia', 'brinco', 'relógio'
    ]
    
    if any(termo in texto_para_analise for termo in termos_beleza_luxo):
        termo_busca = titulo.replace(" ", "+")
        return f"https://www.awin1.com/cread.php?awinaffid={AWIN_ID}&p=https%3A%2F%2Fwww.sephora.com.br%2Fbusca%2F%3Fq%3D{termo_busca}"
    else:
        palavras = titulo.split()[:3]
        termo_busca = "+".join(palavras)
        return f"https://www.amazon.com.br/s?k={termo_busca}&tag={AMAZON_TAG}"

@app.route('/')
def home():
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM noticias ORDER BY id DESC")
        noticias_raw = cursor.fetchall()
        
        noticias = []
        for n in noticias_raw:
            noticia = dict(n)
            # Passando a categoria para a função de gerar_link
            noticia['link_produto'] = gerar_link(noticia['titulo'], noticia.get('categoria', ''))
            noticias.append(noticia)
        conexao.close()
    except Exception as erro:
        print(f"Erro: {erro}")
        noticias = []
    return render_template('index.html', noticias=noticias)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q', '')
    noticias = []
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        query = "SELECT * FROM noticias WHERE titulo LIKE ? OR categoria LIKE ? ORDER BY id DESC"
        cursor.execute(query, ('%' + termo + '%', '%' + termo + '%'))
        noticias_raw = cursor.fetchall()
        
        for n in noticias_raw:
            noticia = dict(n)
            # Passando a categoria aqui também
            noticia['link_produto'] = gerar_link(noticia['titulo'], noticia.get('categoria', ''))
            noticias.append(noticia)
        conexao.close()
    except Exception as erro:
        print(f"Erro na busca: {erro}")
    
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)