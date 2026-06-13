import json
import os

CACHE_FILE = 'noticias_cache.json'

def salvar_cache(dados):
    """Salva as notícias processadas no arquivo JSON."""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print("Cache atualizado com sucesso!")

def carregar_cache():
    """Carrega as notícias do arquivo JSON para exibir no site."""
    if not os.path.exists(CACHE_FILE):
        return {"bilionarios": [], "celebridades": [], "luxo": []}
    
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
