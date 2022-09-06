from classes.Pessoa import Pessoa


class PessoaFisica(Pessoa):
    def __init__(self, documento, nome='', idade=0):
        super().__init__(documento, nome, idade)

    def get_tres_ultimos_digitos_cpf(self):
        return print(f'Os três últimos digitos do cpf são: {self.documento[-3:]}')
