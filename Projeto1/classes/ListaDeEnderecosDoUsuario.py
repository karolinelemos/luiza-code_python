from pydantic import BaseModel
from classes.Endereco import Endereco
from typing import List

# Classe representando a lista de endereços de um cliente


class ListaDeEnderecosDoUsuario(BaseModel):
    id_usuario: int
    enderecos: List[Endereco] = []
