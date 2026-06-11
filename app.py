import sqlite3
from flask import Flask, render_template
import urllib.parse

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
AMAZON_TAG = "midasvip-20"
# Substitua pelo seu ID real da Awin
AWIN_PUBLISHER_ID = "SEU_ID_AWIN_AQUI" 

def obter_conexao_banco():
    conexao = sqlite3.connect('midasvip_definitivo.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def determinar_link(titulo):
    titulo_lower = titulo.lower()
    
    # Palavras-chave que definem produtos de beleza para a Sephora
    termos_beleza = ['beleza', 'perfume', 'maquiagem', 'batom', 'skincare', 'sephora', 'creme', 'cosmético']
    
    if any(termo in titulo_lower for termo in termos_beleza):
        # Rota para AWIN/Sephora
        # O link abaixo é um exemplo padrão de DeepLink da Awin
        url_alvo = urllib.parse.quote("https://www.sephora.com.br/busca/?q=" + titulo)
        return f"https://www.awin1.com/cread.php?awinaffid={AWIN_PUBLISHER_ID}&p={url_alvo}"
    else:
        # Rota para Amazon
        titulo_limpo = titulo.replace('"', '').replace("'", "").replace(":", "")
        termo_curto = " ".join(titulo_limpo.split()[:4])
        termo_busca = urllib.parse.quote(termo_curto)
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
            # Define o link dinamicamente baseado no conteúdo
            noticia['link_produto'] = determinar_link(noticia['titulo'])
            noticias.append(noticia)
            
        conexao.close()
    except Exception as erro:
        print(f"Erro ao processar: {erro}")
        noticias = []

    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)