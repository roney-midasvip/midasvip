import requests
import json

# PREENCHA SUAS CHAVES AQUI
API_KEY = "lmd_dev_F8K39DzOwG_Z1pGoeCk7rg1FFouHbuEdXFldOGfsIWc"
SOURCE_ID = "fc89b7ba-30c3-4ff4-ad37-5ebfea125368"

def atualizar_produtos():
    # Lista das categorias que temos no site
    categorias = ["perfumes", "beleza", "moda feminina", "relogios", "bolsas", "moda masculina", "tecnologia", "viagens"]
    base_produtos = {}

    print("Iniciando busca de produtos...")

    for categoria in categorias:
        # A API da Lomadee busca os produtos automaticamente baseada na palavra-chave
        url = f"https://api.lomadee.com/v3/{API_KEY}/product/_preferred?sourceId={SOURCE_ID}&keyword={categoria}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                # Extrai apenas os produtos, limitando a 5 por categoria para não ficar pesado
                lista_produtos = dados.get('products', [])[:5]
                
                base_produtos[categoria.replace(" ", "-")] = [
                    {
                        "nome": p.get('productName', 'Produto'),
                        "descricao": p.get('shortDescription', 'Aproveite esta oferta exclusiva.'),
                        "link": p.get('link', '#')
                    }
                    for p in lista_produtos
                ]
                print(f"Sucesso: {categoria} adicionada.")
            else:
                print(f"Erro na API ao buscar {categoria}: {response.status_code}")
        
        except Exception as e:
            print(f"Erro de conexão ao buscar {categoria}: {e}")

    # Salva tudo no arquivo para o site ler
    with open('produtos_data.json', 'w', encoding='utf-8') as f:
        json.dump(base_produtos, f, ensure_ascii=False, indent=4)
    
    print("Concluído! O arquivo produtos_data.json foi atualizado.")

if __name__ == "__main__":
    atualizar_produtos()
