import sqlite3
from flask import Flask, render_template
import urllib.parse

app = Flask(__name__)

# Configurações
AMAZON_TAG = "midasvip-20"
# Substitua pelo seu ID da AWIN abaixo
AWIN_ID = "SEU_ID_AWIN_AQUI" 

def obter_conexao_banco():
    conexao = sqlite3.connect('midasvip_definitivo.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def gerar_link_inteligente(titulo):
    titulo_lower = titulo.lower()
    
    # 1. Rota para AWIN/Sephora
    termos_beleza = ['beleza', 'perfume', 'maquiagem', 'batom', 'skincare', 'sephora', 'creme', 'cosmético']
    if any(termo in titulo_lower for termo in termos_beleza):
        # Link simplificado para Awin
        return f"https://www.awin1.com/cread.php?awinaffid={AWIN_ID}&p=https%3A%2F%2Fwww.sephora.com.br%2F"
    
    # 2. Rota para Amazon (Mais genérica para evitar erro de "Nenhum resultado")
    else:
        # Pegamos apenas as 3 primeiras palavras do título para evitar erros de busca
        palavras = titulo.split()[:3]
        termo_curto = "+".join(palavras)
        return f"https://www.amazon.com.br/s?k={termo_curto}&tag={AMAZON_TAG}"

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
            noticia['link_produto'] = gerar_link_inteligente(noticia['titulo'])
            noticias.append(noticia)
            
        conexao.close()
    except Exception as erro:
        print(f"Erro no processamento: {erro}")
        noticias = []

    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)