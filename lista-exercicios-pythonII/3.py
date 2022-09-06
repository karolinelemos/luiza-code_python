from classes.PessoaJuridica import PessoaJuridica

documento = input('Informe o nro do CNPJ: ')

pessoa1 = PessoaJuridica(documento)
pessoa1.get_documento()
