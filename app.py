import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

# Configurações
AMAZON_TAG = "midasvip-20"
AWIN_ID = "2930251"  # Seu ID inserido corretamente

def obter_conexao_banco():
    conexao = sqlite3.connect('midasvip_definitivo.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def gerar_link(titulo):
    titulo_limpo = titulo.lower()
    
    # Lista de termos que direcionam para Sephora/Awin
    termos_beleza = ['beleza', 'perfume', 'maquiagem', 'batom', 'skincare', 'sephora', 'creme', 'cosmético', 'cabelo']
    
    if any(termo in titulo_limpo for termo in termos_beleza):
        # Link Awin para Sephora com seu ID 2930251
        termo_busca = titulo.replace(" ", "+")
        return f"https://www.awin1.com/cread.php?awinaffid={AWIN_ID}&p=https%3A%2F%2Fwww.sephora.com.br%2Fbusca%2F%3Fq%3D{termo_busca}"
    
    else:
        # Link Amazon com sua tag midasvip-20
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
            noticia['link_produto'] = gerar_link(noticia['titulo'])
            noticias.append(noticia)
            
        conexao.close()
    except Exception as erro:
        print(f"Erro: {erro}")
        noticias = []

    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)