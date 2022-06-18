from time import sleep
from .models import Alerta
import yfinance as yf
from django.core.mail import send_mail


def checaPreco(novo_alerta):

    msg_venda = ("{} - preço de VENDA R${} foi atingido.").format(novo_alerta[1], novo_alerta[3]) #ticker, venda
    msg_compra = ("{} - preço de COMPRA R${} foi atingido.").format(novo_alerta[1], novo_alerta[2]) #ticker, compra
    msg_fim = ('Sua operação com {} terminou!').format(novo_alerta[1]) #ticker

    ticker = yf.Ticker(novo_alerta[1]+".SA") #ativo

    i=0
    while i < novo_alerta[5]: #duracao

        cotacao = round(ticker.info['regularMarketPrice'], 2)
        
        if cotacao <= float(novo_alerta[2]): #compra
            # send email compra
            send_mail('StockWatch Alerta!', msg_compra,'admin@stockwatch.com',
                            [novo_alerta[0]], fail_silently=False,) #email

        elif cotacao >= float(novo_alerta[3]): #venda
            # send email venda
            send_mail('StockWatch Alerta!', msg_venda,'admin@stockwatch.com',
                            [novo_alerta[0]], fail_silently=False,) #email

        else:
            pass

        sleep(novo_alerta[4]) #periodo
    
    send_mail('StockWatch Alerta!', msg_fim,'admin@stockwatch.com',
                            [novo_alerta[0]], fail_silently=False,) #email


def pegaAlertas(): ## working
    
    novo_alerta = []
    # todos os alertas:
    alertas = Alerta.objects.all()
    
    # pega de 1 em 1
    for i in alertas:
        email = i.email
        ativo = i.ativo.ticker
        compra = i.compra
        venda = i.venda
        periodo = i.periodo
        duracao = i.duracao

                ##      str     str   float  float    int      int
        novo_alerta = [email, ativo, compra, venda, periodo, duracao]
                ##       0       1      2       3       4       5 

        checaPreco(novo_alerta)
    





