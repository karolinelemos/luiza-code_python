class Pessoa:
    def __init__(self, documento, nome='', idade=0):
        self.documento = documento
        self.nome = nome
        self.idade = idade

    def get_documento(self):
        return print(f'O nro do cpf é {self.documento}')

    def get_nome(self):
        return print(f'Nome: {self.nome}')

    def get_tipo_pessoa(self, f):
        if (f != 'F' and f != 'N'):
            return print('Tipo inválido')

        condicional = 'é' if f == 'F' else 'não é'
        return print(f'{self.nome} {condicional} fumante')
