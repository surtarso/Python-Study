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
    """
    Pega os ativos selecionados em stockpicker e busca suas
    cotacoes para exibir em stocktracker. Adiciona os ativos para o 
    celery para atualizacao em tempo real e para multiplos usuarios
    caso mais de um usuario precise da cotacao do mesmo ativo.

    Args:
        stockpicker (List): escolha de ativos feita em stockpicker

    Returns:
        String: done.
    """
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


##--------------------------------[NO SMTP CONF YET]--------E-MAILS:
def iniciaOperacao(novo_alerta):
    """
    Pega um novo alerta e comeca a operacao de checar a cotacao e mandar
    email para o usuario caso o preco atinja um valor desejado.

    Args:
        novo_alerta (List): itens de um alerta: email, ativo, precos, duracoes.
    """
    print('recebi alerta: {}'.format(novo_alerta))

    email_to = novo_alerta[0]
    ativo = yf.Ticker(novo_alerta[1]+".SA")
    preco_compra = float(novo_alerta[2])
    preco_venda = float(novo_alerta[3])
    periodo = int(novo_alerta[4]) * 60  #periodo em minutos
    duracao = int(novo_alerta[5]) * 86400  #duracao em dias

    msg_venda = ("{} - preço de VENDA R${} foi atingido.").format(ativo, preco_venda)
    msg_compra = ("{} - preço de COMPRA R${} foi atingido.").format(ativo, preco_compra)
    msg_fim = ('Sua operação com {} terminou!').format(ativo)

    i = 0
    while i < duracao: 
        print('faltam {} dias para o fim desta operacao'.format(duracao/86400))

        cotacao = round(ativo.info['regularMarketPrice'], 2)
        print('peguei cotacao: {} - R$ {}'.format(ativo.ticker, cotacao))
        
        if cotacao <= preco_compra:
            send_mail('StockWatch Alerta!', msg_compra,'admin@stockwatch.com',
                            [email_to], fail_silently=True,)

        elif cotacao >= preco_venda:
            send_mail('StockWatch Alerta!', msg_venda,'admin@stockwatch.com',
                            [email_to], fail_silently=True,)
        else:
            pass
        
        print('dormindo: {} - {}min'.format(ativo.ticker, periodo/60))
        sleep(periodo) 
        duracao -= periodo

    print('fim de operacao com {}'.format(ativo.ticker))
    send_mail('StockWatch Alerta!', msg_fim,'admin@stockwatch.com',
                            [email_to], fail_silently=True,) #email

## TODO: add exception for tasks that already exist

@shared_task(bind = True)
def pegaAlertas(self):
    """
    É acionado quando um usuario cria um novo alerta ou altera
    um alerta existente. Não recebe nenhum argumento nem retorna nada.
    Separa todos os alertas da DB em threads e chama a busca de preço
    individualmente.
    """
    print('pegaAlertas: fui acionado')
    # lista com cada alerta individual
    novo_alerta = []
    # lista com todos os alertas individuais acima
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
            arg1: q.put([todos_os_alertas[i], iniciaOperacao(arg1)]),
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