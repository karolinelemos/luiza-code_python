from unittest import result
from xxlimited import Null
from fastapi import FastAPI

# classes
from classes.Endereco import Endereco
from classes.Usuario import Usuario
from classes.ListaDeEnderecosDoUsuario import ListaDeEnderecosDoUsuario
from classes.Produto import Produto
from classes.CarrinhoDeCompras import CarrinhoDeCompras
##


app = FastAPI()

OK = "OK"
FALHA = "FALHA"

db_usuarios = {}
db_produtos = {}
db_end = []        # enderecos_dos_usuarios
db_carrinhos = []

# Criar um usuário,
# se tiver outro usuário com o mesmo ID retornar falha,
# se o email não tiver o @ retornar falha,
# senha tem que ser maior ou igual a 3 caracteres,
# senão retornar OK


def novo_usuario(usuario: Usuario):
    db_usuarios[usuario.id] = usuario
    db_end.append(ListaDeEnderecosDoUsuario(id_usuario=usuario.id))
    db_carrinhos.append(CarrinhoDeCompras(
        id_usuario=usuario.id,
        preco_total=0.00,
        quantidade_de_produtos=0
    ))
    return OK


def valida_usuario(usuario: Usuario):
    if '@' not in usuario.email or len(usuario.senha) < 3:
        return FALHA
    return novo_usuario(usuario)


@app.post("/usuario/")
async def criar_usuário(usuario: Usuario):
    if usuario.id in db_usuarios:
        return FALHA

    return valida_usuario(usuario)


# Se o id do usuário existir, retornar os dados do usuário
# senão retornar falha
@app.get("/usuario/")
async def retornar_usuario(id: int):
    if id in db_usuarios:
        return db_usuarios[id]
    return FALHA


# Se existir um usuário com exatamente o mesmo nome, retornar os dados do usuário
# senão retornar falha
@app.get("/usuario/nome")
async def retornar_usuario_com_nome(nome: str):
    resultado = []
    for item in db_usuarios.values():
        primeiro_nome = item.nome.split()[0].upper()
        if primeiro_nome == nome.upper():
            resultado.append(item)
        continue

    return resultado if len(resultado) else FALHA


# Se o id do usuário existir, deletar o usuário e retornar OK
# senão retornar falha
# ao deletar o usuário, deletar também endereços e carrinhos vinculados a ele
def deleta_usuario(id: int):
    del db_usuarios[id]


def deleta_enderecos(id: int):
    for endereco in db_end:
        if endereco.id_usuario == id:
            db_end.remove(endereco)
        continue


def deleta_carrinhos(id: int):
    for carrinho in db_carrinhos:
        if carrinho.id_usuario == id:
            db_carrinhos.remove(carrinho)
        continue


@app.delete("/usuario/")
async def deletar_usuario(id: int):
    if id in db_usuarios:
        deleta_usuario(id)
        deleta_enderecos(id)
        deleta_carrinhos(id)
        return OK
    return FALHA

# Se não existir usuário com o id_usuario retornar falha,
# senão retornar uma lista de todos os endereços vinculados ao usuário
# caso o usuário não possua nenhum endereço vinculado a ele, retornar
# uma lista vazia
# Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)


def busca_endereco_pelo_usuario(id_usuario: int):
    return list(
        filter(lambda end: end.id_usuario == id_usuario, db_end))


@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    if id_usuario not in db_usuarios:
        return FALHA
    else:
        enderecos = busca_endereco_pelo_usuario(id_usuario)
        return enderecos[0].enderecos

# Retornar todos os emails que possuem o mesmo domínio
# (domínio do email é tudo que vêm depois do @)
# senão retornar falha


@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    emails = list(filter(lambda usuario: usuario.email.split(
        '@')[1].upper() == dominio.upper(), db_usuarios.values()))

    if len(emails):
        return emails
    else:
        return FALHA


# Se não existir usuário com o id_usuario retornar falha,
# senão cria um endereço, vincula ao usuário e retornar OK

def busca_index_endereco(id_usuario: int):
    endereco = busca_endereco_pelo_usuario(id_usuario)
    return db_end.index(endereco[0])


@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Endereco, id_usuario: int):
    if id_usuario not in db_usuarios:
        return FALHA
    else:
        index = busca_index_endereco(id_usuario)
        enderecos = db_end[index].enderecos
        enderecos.append(endereco)

        db_end[index].enderecos = enderecos
        return OK

# Se não existir endereço com o id_endereco retornar falha,
# senão deleta endereço correspondente ao id_endereco e retornar OK
# (lembrar de desvincular o endereço ao usuário)


def busca_indices_enderecos(id_endereco: int):
    for endereco in db_end:
        for end in endereco.enderecos:
            if (end.id == id_endereco):
                return {
                    'index_endereco': db_end.index(endereco),
                    'index_enderecos': endereco.enderecos.index(end)
                }


@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
    indices = busca_indices_enderecos(id_endereco)
    if not indices:
        return FALHA
    db_end[indices["index_endereco"]].enderecos.pop(indices["index_enderecos"])
    return OK

# # Se tiver outro produto com o mesmo ID retornar falha,
# # senão cria um produto e retornar OK


@app.post("/produto/")
async def criar_produto(produto: Produto):
    if produto.id in db_produtos:
        return FALHA
    db_produtos[produto.id] = produto
    return OK

# Se não existir produto com o id_produto retornar falha,
# # senão retorna o produto


@app.get("/produto/{id_produto}/")
async def criar_produto(id_produto: int):
    if id_produto not in db_produtos:
        return FALHA
    return db_produtos[id_produto]

# Se não existir produto com o id_produto retornar falha,
# senão deleta produto correspondente ao id_produto e retornar OK
# (lembrar de desvincular o produto dos carrinhos do usuário)


def remove_produto_dos_carrinhos(id_produto: int):
    for carrinho in db_carrinhos:
        for produto in carrinho.id_produtos:
            if (produto.id == id_produto):
                index_carrinho = db_carrinhos.index(carrinho)
                index_produtos = carrinho.id_produtos.index(produto)
                db_carrinhos[index_carrinho].id_produtos.pop(index_produtos)
                db_carrinhos[index_carrinho].preco_total -= produto.preco
                db_carrinhos[index_carrinho].quantidade_de_produtos -= 1


@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    if id_produto not in db_produtos:
        return FALHA
    remove_produto_dos_carrinhos(id_produto)
    db_produtos.pop(id_produto)
    return OK

# Se não existir usuário com o id_usuario ou id_produto retornar falha,
# se não existir um carrinho vinculado ao usuário, crie o carrinho
# e retornar OK
# senão adiciona produto ao carrinho e retornar OK


def busca_indice_carrinho(id_usuario: int):
    for carrinho in db_carrinhos:
        if carrinho.id_usuario == id_usuario:
            return db_carrinhos.index(carrinho)


def verifica_carrinho_usuario(id_usuario: int):
    index = busca_indice_carrinho(id_usuario)
    if index is None:
        db_carrinhos.append(CarrinhoDeCompras(
            id_usuario=id_usuario,
            preco_total=0.00,
            quantidade_de_produtos=0
        ))


def adiciona_produto_no_carrinho(id_usuario: int, id_produto: int):
    index = busca_indice_carrinho(id_usuario)
    carrinho = db_carrinhos[index]
    produto = db_produtos[id_produto]

    carrinho.quantidade_de_produtos += 1
    carrinho.id_produtos.append(produto)
    carrinho.preco_total += produto.preco

    db_carrinhos[index] = CarrinhoDeCompras(
        preco_total=carrinho.preco_total,
        id_usuario=id_usuario,
        quantidade_de_produtos=carrinho.quantidade_de_produtos,
        id_produtos=carrinho.id_produtos
    )


@app.post("/carrinho/{id_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
    if id_usuario not in db_usuarios or id_produto not in db_produtos:
        return FALHA
    verifica_carrinho_usuario(id_usuario)
    adiciona_produto_no_carrinho(id_usuario, id_produto)
    return OK

# Se não existir carrinho com o id_usuario retornar falha,
# senão retorna o carrinho de compras.


@app.get("/carrinho/{id_usuario}/details")
async def retornar_carrinho(id_usuario: int):
    index = busca_indice_carrinho(id_usuario)
    if index is None:
        return FALHA
    return db_carrinhos[index]

# Se não existir carrinho com o id_usuario retornar falha,
# senão retorna o o número de itens e o valor total do carrinho de compras.


@app.get("/carrinho/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int):
    index = busca_indice_carrinho(id_usuario)
    if index is None:
        return FALHA
    return f'numero itens: {db_carrinhos[index].quantidade_de_produtos} | valor_total: {db_carrinhos[index].preco_total}R$'

# Se não existir usuário com o id_usuario retornar falha,
# senão deleta o carrinho correspondente ao id_usuario e retornar OK


@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    if not id_usuario in db_usuarios:
        return FALHA
    index = busca_indice_carrinho(id_usuario)
    if index is None:
        return OK
    db_carrinhos.pop(index)
    return OK


@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')
