import asyncio
from sys import hash_info
from celery import shared_task
from threading import Thread
import queue
from channels.layers import get_channel_layer
import simplejson as json
from time import sleep
from django.core.mail import send_mail
# yahoo api
from yahoo_fin.stock_info import *
import yfinance as yf
# models
from .models import Alerta


##----------------------------------------------- LIVE STOCKS INFO:
# funcoes associadas ao celery:
@shared_task(bind = True)
def update_stock(self, stockpicker):
    data = {}
    available_stocks = tickers_ibovespa()

    # remove acoes que n estao sendo mais solicitadas:
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            stockpicker.remove(i)
    
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()

    for i in range(n_threads):
        thread = Thread(
            target = lambda q,
            arg1: q.put({stockpicker[i]: json.loads(json.dumps(get_quote_table(arg1+'.SA'), ignore_nan = True))}),
            args = (que, stockpicker[i])
            )
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        result = que.get()
        data.update(result)

    # manda update das acoes existentes:
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type':'send_stock_update',
        'message':data,
    }))

    return 'update_stock() -> Done.'

##----------------------------------------------------------------





##---------------------------------------------[NO SMTP CONF YET]--E-MAILS:

## ------------->  str    str    float  float     int     int
## novo_alerta = [email, ativo, compra, venda, periodo, duracao]
## ------------->   0      1      2       3       4        5 
def checaPreco(novo_alerta):
    print('recebi alerta: {}'.format(novo_alerta))
    msg_venda = ("{} - preço de VENDA R${} foi atingido.").format(novo_alerta[1], novo_alerta[3]) #ticker, venda
    msg_compra = ("{} - preço de COMPRA R${} foi atingido.").format(novo_alerta[1], novo_alerta[2]) #ticker, compra
    msg_fim = ('Sua operação com {} terminou!').format(novo_alerta[1]) #ticker

    ticker = yf.Ticker(novo_alerta[1]+".SA") #ativo

    i=0
    while i < (novo_alerta[5]*86400): #duracao em dias
        print('duracao: {}'.format(novo_alerta[5]))

        cotacao = round(ticker.info['regularMarketPrice'], 2)
        print('peguei cotacao: {} - R$ {}'.format(ticker.ticker, cotacao))
        
        if cotacao <= float(novo_alerta[2]): #compra
            # send email compra
            send_mail('StockWatch Alerta!', msg_compra,'admin@stockwatch.com',
                            [novo_alerta[0]], fail_silently=True,) #email

        elif cotacao >= float(novo_alerta[3]): #venda
            # send email venda
            send_mail('StockWatch Alerta!', msg_venda,'admin@stockwatch.com',
                            [novo_alerta[0]], fail_silently=True,) #email

        else:
            pass
        
        print('dormindo: {} - {}seg(s)'.format(ticker.ticker, novo_alerta[4]))
        sleep(novo_alerta[4]*60) #periodo em minutos
        novo_alerta[5] -= 1

    print('fim de operacao com {}'.format(ticker.ticker))
    send_mail('StockWatch Alerta!', msg_fim,'admin@stockwatch.com',
                            [novo_alerta[0]], fail_silently=True,) #email
    
    # data = {'ticker': ticker.info}
    # return data



@shared_task(bind = True)
def pegaAlertas(self):
    print('pegaAlertas: fui acionado')
    # lista com cada alerta individual
    novo_alerta = []
    # lista com todos os alertas individuais
    todos_os_alertas = []
    # todos os alertas da database:
    alertas = Alerta.objects.all()

    # itera de 1 em 1
    for i in alertas:
        email = str(i.email)
        ativo = str(i.ativo.ticker)
        compra = float(i.compra)
        venda = float(i.venda)
        periodo = int(i.periodo)
        duracao = int(i.duracao)

        novo_alerta = [email, ativo, compra, venda, periodo, duracao]

        ## todo: add exception for tasks that already exist
        todos_os_alertas.append(novo_alerta)
    
    # numero de threads = numero de alertas disponiveis
    n_threads = len(todos_os_alertas)
    # lista com as threads
    thread_list = []
    # fila
    que = queue.Queue()


    # itera com o numero de alertas disponiveis
    for i in range(n_threads):
        thread = Thread(
            target = lambda q,
            arg1: q.put([todos_os_alertas[i], checaPreco(arg1)]),
            args = (que, todos_os_alertas[i])
            )
        # adiciona resposta do item a lista de threads
        thread_list.append(thread)
        # inicia tal thread
        thread_list[i].start()

    # itera por todas as threads na threadlist
    for thread in thread_list:
        # une as threads
        thread.join()
    
    # enquanto a fila de threads nao estiver vazia
    while not que.empty():
        #pega o proximo da fila
        que.get()

    return 'No mail tasks left'