import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def obter_conexao_banco():
    conexao = sqlite3.connect('midasvip_definitivo.db')
    conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    return conexao

@app.route('/')
def home():
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        
        # Busca todas as notícias salvas pelo seu robô
        cursor.execute("SELECT * FROM noticias ORDER BY id DESC")
        noticias_cadastradas = cursor.fetchall()
        
        conexao.close()
    except Exception as erro:
        print(f"Erro ao conectar ou buscar dados: {erro}")
        noticias_cadastradas = []

    return render_template('index.html', noticias=noticias_cadastradas)

# Essa linha final é essencial para o Render conseguir ligar o servidor web
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)