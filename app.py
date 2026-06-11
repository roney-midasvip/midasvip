import sqlite3
from flask import Flask, render_template
import urllib.parse

app = Flask(__name__)

# Configuração da sua tag de afiliado
AMAZON_TAG = "midasvip-20"

def obter_conexao_banco():
    # Conecta ao seu banco de dados
    conexao = sqlite3.connect('midasvip_definitivo.db')
    conexao.row_factory = sqlite3.Row
    return conexao

@app.route('/')
def home():
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        
        # Busca todas as notícias
        cursor.execute("SELECT * FROM noticias ORDER BY id DESC")
        noticias_raw = cursor.fetchall()
        
        noticias = []
        for n in noticias_raw:
            noticia = dict(n)
            
            # Lógica para tratar o título e evitar erros de busca na Amazon
            # Removemos caracteres especiais que costumam quebrar a busca
            titulo_limpo = noticia['titulo'].replace('"', '').replace("'", "")
            termo_busca = urllib.parse.quote(titulo_limpo)
            
            # Gera o link formatado corretamente para a Amazon
            noticia['link_produto'] = f"https://www.amazon.com.br/s?k={termo_busca}&tag={AMAZON_TAG}"
            
            noticias.append(noticia)
            
        conexao.close()
    except Exception as erro:
        print(f"Erro ao processar dados: {erro}")
        noticias = []

    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)