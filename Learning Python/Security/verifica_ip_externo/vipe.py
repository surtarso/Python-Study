import re  #expressoes regulares
import json
from urllib.request import urlopen


url = 'https://ipinfo.io/json'
#abre a url
resposta = urlopen(url)
#carrega resposta
dados = json.load(resposta)

ip = dados['ip']
org = dados['org']
cid = dados['city']
pais = dados['country']
regiao = dados['region']

print('detalhes do ip:')
print('IP: {4}\nRegiao: {1}\nPais: {2}\nCidade: {3}\nOrg.: {0}'.format(org,regiao,pais,cid,ip))
