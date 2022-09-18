from pydantic import BaseModel

# Classe representando os dados do endereço do cliente


class Endereco(BaseModel):
    id: int
    rua: str
    cep: str
    cidade: str
    estado: str
