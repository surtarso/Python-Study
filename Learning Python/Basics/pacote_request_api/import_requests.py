## pacote instalado pelo pip install requests
## serve para HTTP requests
import requests

def retorna_dados_cep(cep):
    response = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep))
    print(response.status_code) ## 200! sucesso
    # print(response.text) ## recebe em string
    # print(type(response.text)) ## string
    # print(response.json()) ## recebe em json
    # print(type(response.json())) ## no tipo dicionario key/value
    dados_cep = response.json()
    # print(dados_cep['cep'])
    # print(dados_cep['logradouro'])
    return dados_cep

def retorna_response(url):
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    # print(retorna_dados_cep('22793268'))
    response = retorna_response('https://google.com')
    print(response) ## puxa o HTML da pagina em texto


