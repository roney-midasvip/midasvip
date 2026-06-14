from flask import Flask, render_template
from noticias_manager import carregar_cache
import requests

app = Flask(__name__)

API_KEY = "lmd_dev_F8K39DzOwG_Z1pGoeCk7rg1FFouHbuEdXFldOGfsIWc"
API_URL = "https://api-beta.lomadee.com.br/affiliate/products"

ORGS = {
    "drogaria_rosario": "1fcee90e-562e-455c-97a5-6bdd6d60b589",
    "le_loyn": "09562538-fde7-4bbf-947b-2ccebbc1c887",
    "sieno": "a4ea6ed5-0ffd-4ee7-b0eb-f6073dc4fc12",
    "simple_organic": "e783798e-b219-48d6-9855-a7ad62d1d2c6",
    "guess": "836cf386-910f-4065-a9d5-bfb1d18731d6",
    "morena_rosa": "20ead81f-493b-45a7-8ab6-5f523d4df803",
    "le_postiche": "46799ce3-0050-4047-b92c-0dc558b97597",
    "lenovo": "2db74df3-f709-489e-819b-9212e698bd81",
    "xiaomi": "e1d43df5-8c98-4f7a-9f75-e507ecbd649c",
    "freeway": "2e9c32ff-43f2-46d8-8b08-339114067bcd",
    "camisaria_colombo": "6b5363cb-94b8-42ee-8938-b71a1234eb08"
}


def buscar_produtos(search="", organization_ids=None, limite=24, preco_min=200):
    try:
        headers = {
            "x-api-key": API_KEY
        }

        params = {
            "page": 1,
            "limit": 100,
            "price": f"{preco_min * 100}:99999999",
            "isAvailable": "true"
        }

        if search:
            params["search"] = search

        if organization_ids:
            if isinstance(organization_ids, list):
                params["organizationIds"] = ",".join(organization_ids)
            else:
                params["organizationIds"] = organization_ids

        r = requests.get(API_URL, headers=headers, params=params, timeout=20)

        if r.status_code != 200:
            print("Erro LinkMyDeals:", r.status_code, r.text[:500])
            return []

        produtos = r.json().get("data", [])

        produtos_filtrados = []
        nomes_vistos = set()

        for item in produtos:
            nome = item.get("name", "").strip()
            url = item.get("url", "").strip()
            imagens = item.get("images", [])
            options = item.get("options", [])

            if not nome or not url or not imagens or not options:
                continue

            pricing = options[0].get("pricing", [])

            if not pricing:
                continue

            preco = pricing[0].get("price", 0)

            if not preco or preco < preco_min:
                continue

            chave_nome = nome.lower().strip()

            if chave_nome in nomes_vistos:
                continue

            nomes_vistos.add(chave_nome)
            produtos_filtrados.append(item)

            if len(produtos_filtrados) >= limite:
                break

        return produtos_filtrados

    except Exception as e:
        print("Erro ao buscar produtos:", e)
        return []


@app.route("/")
def home():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("index.html", noticias=todas[:8])


@app.route("/noticias")
def noticias():
    dados = carregar_cache()
    todas = dados.get("bilionarios", []) + dados.get("celebridades", []) + dados.get("luxo", [])
    return render_template("noticias.html", noticias=todas)


@app.route("/celebridades")
def celebridades():
    dados = carregar_cache()
    return render_template("celebridades.html", noticias=dados.get("celebridades", []))


@app.route("/bilionarios")
def bilionarios():
    dados = carregar_cache()
    return render_template("bilionarios.html", noticias=dados.get("bilionarios", []))


@app.route("/luxo")
def luxo():
    dados = carregar_cache()
    return render_template("luxo.html", noticias=dados.get("luxo", []))


@app.route("/midasvip-select")
def midasvip_select():
    return render_template("midasvip_select.html")


@app.route("/perfumes")
def perfumes():
    produtos = buscar_produtos(
        search="perfume",
        organization_ids=[
            ORGS["drogaria_rosario"],
            ORGS["le_loyn"],
            ORGS["sieno"]
        ],
        limite=24,
        preco_min=400
    )
    return render_template("perfumes.html", produtos=produtos)


@app.route("/beleza")
def beleza():
    produtos = buscar_produtos(
        search="creme facial",
        organization_ids=[
            ORGS["simple_organic"]
        ],
        limite=24,
        preco_min=80
    )

    if not produtos:
        produtos = buscar_produtos(
            search="skin care",
            organization_ids=[
                ORGS["simple_organic"]
            ],
            limite=24,
            preco_min=80
        )

    return render_template("beleza.html", produtos=produtos)


@app.route("/moda-feminina")
def moda_feminina():
    produtos = buscar_produtos(
        search="vestido",
        organization_ids=[
            ORGS["morena_rosa"]
        ],
        limite=24,
        preco_min=200
    )

    if not produtos:
        produtos = buscar_produtos(
            search="blusa",
            organization_ids=[
                ORGS["morena_rosa"],
                ORGS["guess"]
            ],
            limite=24,
            preco_min=200
        )

    return render_template("moda_feminina.html", produtos=produtos)


@app.route("/relogios")
def relogios():
    produtos = buscar_produtos(
        search="relógio",
        limite=24,
        preco_min=300
    )

    if not produtos:
        produtos = buscar_produtos(
            search="relogio",
            limite=24,
            preco_min=300
        )

    return render_template("relogios.html", produtos=produtos)


@app.route("/bolsas")
def bolsas():
    produtos = buscar_produtos(
        search="bolsa",
        organization_ids=[
            ORGS["guess"],
            ORGS["le_postiche"]
        ],
        limite=24,
        preco_min=250
    )
    return render_template("bolsas.html", produtos=produtos)


@app.route("/moda-masculina")
def moda_masculina():
    produtos = buscar_produtos(
        search="camisa",
        organization_ids=[
            ORGS["freeway"],
            ORGS["camisaria_colombo"]
        ],
        limite=24,
        preco_min=150
    )

    if not produtos:
        produtos = buscar_produtos(
            search="calçado",
            organization_ids=[
                ORGS["freeway"]
            ],
            limite=24,
            preco_min=150
        )

    return render_template("moda_masculina.html", produtos=produtos)


@app.route("/tecnologia")
def tecnologia():
    produtos = buscar_produtos(
        search="notebook",
        organization_ids=[
            ORGS["lenovo"]
        ],
        limite=24,
        preco_min=1000
    )

    if not produtos:
        produtos = buscar_produtos(
            search="smartphone",
            organization_ids=[
                ORGS["xiaomi"]
            ],
            limite=24,
            preco_min=600
        )

    return render_template("tecnologia.html", produtos=produtos)


@app.route("/viagens")
def viagens():
    produtos = buscar_produtos(
        search="mala",
        organization_ids=[
            ORGS["le_postiche"]
        ],
        limite=24,
        preco_min=200
    )
    return render_template("viagens.html", produtos=produtos)


if __name__ == "__main__":
    app.run(debug=True)
