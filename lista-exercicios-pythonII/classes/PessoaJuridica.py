from classes.Pessoa import Pessoa


class PessoaJuridica(Pessoa):
    def __init__(self, documento, nome='', idade=0):
        super().__init__(documento, nome, idade)

    def get_documento(self):
        return print(f'O nro do CNPJ é: {self.documento}')
