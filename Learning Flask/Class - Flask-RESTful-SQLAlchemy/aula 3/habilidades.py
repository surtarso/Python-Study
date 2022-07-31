from flask_restful import Resource



habilidades = ['python', 'flask', 'django', 'javascript']


class ListaHabilidades(Resource):
    # inserir nova habilidade
    def post(self):
        pass
    
    #retornar habilidades existentes
    def get(self):
        return habilidades
    
    #alterar o nome de uma habilidade
    def put(self):
        pass
    
    #deletar uma habilidade
    def delete(self):
        pass