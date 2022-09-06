from classes.Pessoa import Pessoa

nome = input('Informe o nome: ')
documento = input('Informe o nro do CPF: ')
idade = int(input('Informe a idade: '))
tipo = input('Informe (F) para fumante e (N) para não fumante: ')

pessoa1 = Pessoa(documento, nome, idade)
pessoa1.get_documento()
pessoa1.get_nome()
pessoa1.get_tipo_pessoa(tipo)
