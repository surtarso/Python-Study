from flask import Flask, jsonify, request
import json

app = Flask(__name__)



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


@app.route('/dev/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def desenvolvedor(id):
    
    if request.method == 'GET':
        
        try:
            response = desenvolvedores[id]
        except IndexError:
            mensagem = 'dev id {} nao existe'.format(id)
            response = ({'status': 'erro', 'mensagem': mensagem})
        except Exception:
            mensagem = 'erro desconhecido'
            response = ({'status': 'erro', 'mensagem': mensagem})
        
        return jsonify(response)
    
    elif request.method == 'PUT':
        dados = json.loads(request.data)
        desenvolvedores[id] = dados
        
        return jsonify(dados)
    
    elif request.method == 'DELETE':
        desenvolvedores.pop(id)

        return jsonify({'status': 'sucesso', 'mensagem': 'registro excluido'})
          

@app.route('/dev', methods=['POST', 'GET'])
def lista_desenvolvedores():
    
    if request.method == 'POST':
        
        dados = json.loads(request.data)
        posicao = len(desenvolvedores)
        dados['id'] = posicao
        desenvolvedores.append(dados)
        
        return jsonify({'status': 'sucesso', 'mensagem': 'registro incluido', 'dados': desenvolvedores[posicao]})

    elif request.method == 'GET':
        
        return jsonify(desenvolvedores)




if __name__ == "__main__":
    app.run(debug=True)