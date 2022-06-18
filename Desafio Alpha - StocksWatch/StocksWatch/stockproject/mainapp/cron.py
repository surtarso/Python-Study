import queue
from threading import Thread
from time import sleep
from .models import Alerta
import yfinance as yf
from django.core.mail import send_mail
import schedule


###--------------------------- TENTATIVA 1 -------------------------------------

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



def pegaAlertas():  ##funcionando
    
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
    







###--------------------------- TENTATIVA 2 -------------------------------------


def checaPreco_teste2(novo_alerta):

    msg_venda = ("{} - preço de VENDA R${} foi atingido.").format(novo_alerta[1], novo_alerta[3]) #ticker, venda
    msg_compra = ("{} - preço de COMPRA R${} foi atingido.").format(novo_alerta[1], novo_alerta[2]) #ticker, compra
    msg_fim = ('Sua operação com {} terminou!').format(novo_alerta[1]) #ticker

    ticker = yf.Ticker(novo_alerta[1]+".SA") #ativo

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
    
    schedule.every(novo_alerta[5]).minutes.do(checaPreco_teste2)

    while True:
        schedule.run_pending()
        sleep(novo_alerta[4]) #periodo


def pegaAlertas_teste2():  ## nao testado
    
    novo_alerta = {}
    # todos os alertas:
    alertas = Alerta.objects.all()
    
    #teste multithreading
    n_threads = len(alertas)
    thread_list = []
    que = queue.Queue()

    # pega de 1 em 1
    for i in range(n_threads):
        thread = Thread(
            target = checaPreco_teste2,
            args = (
                que,
                alertas[i].email,
                alertas[i].ativo.ticker,
                alertas[i].compra,
                alertas[i].venda,
                alertas[i].periodo,
                alertas[i].duracao
            )
        )
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        novo_alerta.update(result)

    checaPreco_teste2(novo_alerta)