"""
This App will check the current price of a stock on a period and alarm 
the user by e-mail(wip) with buy and sell operations based on user's 
set min/max price for a certain period. It will also display stock price
history with a period set by the user.
Tarso Galvão - 12/06/2022
"""

import yfinance as yf
from time import sleep

# debug toggle
IS_DEBUG = True  # false for real time
DIA = 86400  # 1 dia em segundos

##--recebe email, nome do papel, periodicidade de busca e limite de dias da operacao
email_in = input("insira seu email: ")
papel_in = input("papel B3 para busca: ")
periodo_in = int(input("periodicidade da cotacao em minutos: "))
dias_in = int(input("periodo da operação em dias: ")) 

# formata a busca inserida
if IS_DEBUG:
    periodo = periodo_in  # mantem em segundos para debug
    dias = dias_in * 3  # mantem em um range aceitavel para debug
else:
    periodo = periodo_in * 60  # formata o input para minutos
    dias = dias_in * DIA  # formata o input para dias

ticker = yf.Ticker(papel_in.upper()+".SA") #formata para yahoo
data = ticker.history() #pega historico

# mostra historico min/max
pesquisar = input("\nPesquisar historico de precos? s/n: ")
if pesquisar == "s" or pesquisar == "S":
    print('“1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”')
    print('“1h”, “1d”, “5d”, “1wk”, “1mo”, "1yr", "max"')
    historico = input("Periodo do historico: ")
    print("\n")
    data = ticker.history(period=historico) #limita historico
    low = data["Low"]
    high = data["High"]
    print(low, high)

#mostra recomendacao de compra/venda
pesquisar = input("Gostaria de ver recomendacoes de compra/venda? s/n: ")
if pesquisar == "s" or pesquisar == "S":
    print("Recomendações:")
    print(ticker.recommendations)

print("\nUltimo fechamento:",round(data['Close'].iloc[-1], 2))
##--recebe valores de compra e venda
price_min = float(input("\nvalor de compra: "))
price_max = float(input("valor de venda: "))
# error handling:
while price_min > price_max or price_max == price_min:
    print("Valor da compra tem que ser maior que o valor da venda!\n")
    price_min = float(input("valor de compra: "))
    price_max = float(input("valor de venda: "))

# cria nova lista de cotacoes
cotacoes = []

##--- inicia operacao de busca
print("\nIniciando operação:")
print("-------------------\n")
i = 0
while i != dias:
    #pega preço atual do ticker
    cotacao = round(ticker.info['regularMarketPrice'], 2)
    #insere preço no inicio da tabela
    cotacoes.insert(0, cotacao)

    print("Preço max: ", max(cotacoes))
    print("Atual: ", cotacao)
    print("Preço min: ", min(cotacoes))

    #PLACEHOLDER: adicionar sistema de email
    if cotacao >= price_max:
        print("\nPreço de VENDA atingido---> enviado para:", email_in)
    elif cotacao <= price_min:
        print("\nPreço de COMPRA atingido---> enviado para:", email_in)
    else:
        pass
        #print("\n...mercado lateral...")

    print("...",periodo_in, "min(s) para nova busca...\n")
    sleep(periodo)
    i += 1
#--- finaliza opecarao de busca
print("\nFim de operação")
print("---------------\n")

## PLACEHOLDER: adicionar sistema de email
print("Enviando para", email_in, ":\n--> Dias de operação com", papel_in.upper(), "excedidos, faça uma nova operação.\n")
## PLACEHOLDER: é para gerar uma tabela com esses valores
print("Historico de", dias_in, "dia(s) de operação com", papel_in.upper(),":\n", cotacoes)
