import requests
from googletrans import Translator
from noticias_manager import salvar_cache

# Chave da NewsAPI inserida
API_KEY = '7a1c6708658f493bb44176f431606bc3'
translator = Translator()

def buscar_noticias(query):
    # Endpoint da NewsAPI para buscar em todo o mundo (language=en)
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') == 'ok':
            return data.get('articles', [])[:10] # Pega até 10 notícias por categoria
        else:
            print(f"Erro na API: {data.get('message')}")
            return []
    except Exception as e:
        print(f"Erro na conexão com a API: {e}")
        return []

def processar_noticias():
    # Categorias e palavras-chave para o seu site
    categorias = {
        "bilionarios": "Billionaire OR Forbes OR 'Net worth'",
        "celebridades": "Celebrity OR Hollywood OR Famous",
        "luxo": "Luxury OR 'Luxury lifestyle' OR Supercars OR Rolex"
    }
    
    dados_finais = {}

    for cat, query in categorias.items():
        print(f"Processando categoria: {cat}...")
        artigos = buscar_noticias(query)
        lista_processada = []
        
        for art in artigos:
            # Tradução do título e descrição para português
            try:
                titulo_pt = translator.translate(art['title'], dest='pt').text
                
                lista_processada.append({
                    'titulo': titulo_pt,
                    'link': art['url'],
                    'fonte': art['source']['name'],
                    'imagem': art.get('urlToImage')
                })
            except Exception as e:
                print(f"Erro na tradução: {e}")
                continue
        
        dados_finais[cat] = lista_processada
    
    # Salva no arquivo JSON para o Flask ler
    salvar_cache(dados_finais)

if __name__ == "__main__":
    processar_noticias()
