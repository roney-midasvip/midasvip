import time

CACHE_TEMPO_SEGUNDOS = 60 * 60  # 1 hora
CACHE_MAX_ATUALIZACOES_DIA = 24

cache = {
    "tempo": 0,
    "dados": [],
    "atualizacoes_dia": 0,
    "dia": None
}


def reset_diario():
    hoje = time.strftime("%Y-%m-%d")
    if cache["dia"] != hoje:
        cache["dia"] = hoje
        cache["atualizacoes_dia"] = 0


def pode_atualizar():
    reset_diario()
    return cache["atualizacoes_dia"] < CACHE_MAX_ATUALIZACOES_DIA


def atualizar_cache(novas_noticias):
    reset_diario()

    cache["dados"] = novas_noticias
    cache["tempo"] = time.time()
    cache["atualizacoes_dia"] += 1


def get_cache():
    return cache["dados"]


def cache_valido():
    return time.time() - cache["tempo"] < CACHE_TEMPO_SEGUNDOS
