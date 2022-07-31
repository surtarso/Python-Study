from models import Pessoas, Usuarios


def insere_pessoas():
    pessoa = Pessoas(nome='Tarso', idade=30)
    pessoa.save()


def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)


def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Tarso').first()
    pessoa.nome = 'Pedro'
    pessoa.save()

   
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Pedro').first()
    pessoa.delete()


def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()
    
def consulta_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)


# if __name__ == '__main__':
#     insere_pessoas()
#     altera_pessoa()
#     exclui_pessoa()
#     consulta_pessoas()
#     insere_usuario('tarso', '1234')
#     insere_usuario('mario', '123')
#     consulta_usuarios()
