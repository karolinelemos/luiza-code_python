from pydantic import BaseModel

# Classe representando os dados do cliente


class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    senha: str
