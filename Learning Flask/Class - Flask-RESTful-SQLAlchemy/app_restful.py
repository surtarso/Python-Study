from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

#---------------MOCK------------------
desenvolvedores = [
    {
        'id': 0,
        'nome': 'tarso',
        'habilidades': ['python', 'flask']
    },
    {
        'id': 1,
        'nome': 'joao',
        'habilidades': ['python', 'django']
    }
]
#-------------------------------------

class Desenvolvedor(Resource):
    def get(self, id):
        try:
            response = desenvolvedores[id]
        except IndexError:
            mensagem = 'dev id {} nao existe'.format(id)
            response = ({'status': 'erro', 'mensagem': mensagem})
        except Exception:
            response = ({'status': 'erro', 'mensagem': 'erro desconhecido'})
            
        return response
    
    def put(self, id):
        dados = json.loads(request.data)
        desenvolvedores[id] = dados
        return dados
    
    def delete(self, id):
        desenvolvedores.pop(id)
        return ({'status': 'sucesso', 'mensagem': 'dev excluido'})


class ListaDesenvolvedores(Resource):
    def get(self):
        return desenvolvedores
    
    def post(self):
        dados = json.loads(request.data)
        posicao = len(desenvolvedores)
        dados['id'] = posicao
        desenvolvedores.append(dados)
        
        return ({'status': 'sucesso', 'mensagem': 'registro incluido', 'dados': desenvolvedores[posicao]})
    
    
    
api.add_resource(Desenvolvedor, '/dev/<int:id>')
api.add_resource(ListaDesenvolvedores, '/dev')



if __name__ == '__main__':
    app.run(debug=True)