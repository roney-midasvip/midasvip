from flask import Flask, render_template
import requests
import json
import os

app = Flask(__name__)

# Configurações originais
API_KEY = "lmd_dev_F8K39DzOwG_Z1pGoeCk7rg1FFouHbuEdXFldOGfsIWc"
SOURCE_ID = "fc89b7ba-30c3-4ff4-ad37-5ebfea125368"

def get_products(category):
    # Tenta ler do arquivo local primeiro (fallback de segurança)
    if os.path.exists('produtos_data.json'):
        with open('produtos_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(category, [])
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<category>')
def category_page(category):
    produtos = get_products(category)
    return render_template(f'{category}.html', produtos=produtos, categoria=category)

if __name__ == '__main__':
    app.run(debug=True)
