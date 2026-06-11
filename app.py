import sqlite3
from flask import Flask, render_template
import urllib.parse

app = Flask(__name__)

# Configurações do seu site
AMAZON_TAG = "midasvip-20"

def obter_conexao_banco():
    # Conecta ao seu banco de dados local
    conexao = sqlite3.connect('midasvip_definitivo.db')
    conexao.row_factory = sqlite3.Row
    return conexao

@app.route('/')
def home():
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        
        # Busca todas as notícias salvas
        cursor.execute("SELECT * FROM noticias ORDER BY id DESC")
        noticias_raw = cursor.fetchall()
        
        # Processa as notícias para adicionar o link de produto dinamicamente
        noticias = []
        for n in noticias_raw:
            noticia = dict(n)
            
            # Formata o título da notícia para ser usado na busca da Amazon
            termo_busca = urllib.parse.quote(noticia['titulo'])
            
            # Gera o link de "Oferta Especial" na Amazon
            noticia['link_produto'] = f"https://www.amazon.com.br/s?k={termo_busca}&tag={AMAZON_TAG}"
            
            noticias.append(noticia)
            
        conexao.close()
    except Exception as erro:
        print(f"Erro ao conectar ou buscar dados: {erro}")
        noticias = []

    # Envia as notícias para o seu index.html
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    # Configurado para rodar no Render ou localmente
    app.run(debug=True, host='0.0.0.0', port=5000)