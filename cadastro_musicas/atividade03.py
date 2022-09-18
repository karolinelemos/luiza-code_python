# ======================
# Persistência / Repositório
# ======================
import fastapi
from typing import Optional
import pydantic
MEMORIA_MUSICAS = []


def persistencia_musica_salvar(nova_musica):
    codigo_nova_musica = len(MEMORIA_MUSICAS) + 1
    nova_musica["codigo"] = codigo_nova_musica
    MEMORIA_MUSICAS.append(nova_musica)
    return nova_musica


def persistencia_musica_pesquisar_todas():
    musicas = list(MEMORIA_MUSICAS)
    return musicas


def persistencia_pesquisar_pelo_codigo(codigo):
    musica_procurada = None
    for musica in MEMORIA_MUSICAS:
        if musica["codigo"] == codigo:
            musica_procurada = musica
            break
    return musica_procurada

# ======================
# Regras / Casos de Uso
# ======================


def regras_musica_cadastrar(nova_musica):
    # TODO Validar a nova musica
    # regras_musica_validar_nova_musica(nova_musica)
    # persistencia_musica_salvar(nova_musica)
    nova_musica = persistencia_musica_salvar(nova_musica)
    return nova_musica


def regras_musica_pesquisar_todas():
    return persistencia_musica_pesquisar_todas()


def regras_musica_pesquisar_pelo_codigo(codigo):
    return persistencia_pesquisar_pelo_codigo(codigo)

# ======================
# API Rest / Controlador
# ======================


aplicacao_web = fastapi.FastAPI()

# --- rotas ---


@aplicacao_web.get("/")
def rota_raiz():
    return {
        "ok": True,
        "versao": "Fase 1"
    }


# ** Rota músicas **


class NovaMusica(pydantic.BaseModel):
    nome: str
    artista: str
    tempo: Optional[int]


@aplicacao_web.post("/musicas")
def rota_musica_cadastrar(nova_musica: NovaMusica):
    nova_musica = regras_musica_cadastrar(nova_musica.dict())
    print("Registrando nova musica",  nova_musica)


@aplicacao_web.get("/musicas")
def rota_musica_pesquisar_todas():
    return regras_musica_pesquisar_todas()


@aplicacao_web.get("/musicas/{codigo}")
def rota_musica_pesquisar_pelo_codigo(codigo: int):
    return regras_musica_pesquisar_pelo_codigo(codigo)
