class Professor:
    def __init__(self, nome, idade, salario):
        self.nome = nome
        self.idade = idade
        self.salario = salario

    def __get_salario(self):
        return print(f'O salário é de R${self.salario}')

    def get_salario(self):
        usuario = input(
            f'Para ver o salário do prof {self.nome}, informe o usuário: ')
        if (usuario == 'usr12'):
            return self.__get_salario()

        return print('Usuário não autorizado')
