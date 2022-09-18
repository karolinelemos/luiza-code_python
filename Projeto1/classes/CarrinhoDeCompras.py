from pydantic import BaseModel
from classes.Produto import Produto
from typing import List

# Classe representando o carrinho de compras de um cliente com uma lista de produtos


class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    id_produtos: List[Produto] = []
    preco_total: float
    quantidade_de_produtos: int
