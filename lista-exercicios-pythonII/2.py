from classes.PessoaFisica import PessoaFisica

nome = input('Informe o nome: ')
documento = input('Informe o nro do CPF: ')
idade = int(input('Informe a idade: '))
tipo = input('Informe (F) para fumante e (N) para não fumante: ')

pessoa1 = PessoaFisica(documento, nome, idade)
pessoa1.get_documento()
pessoa1.get_nome()
pessoa1.get_tipo_pessoa(tipo)
pessoa1.get_tres_ultimos_digitos_cpf()
