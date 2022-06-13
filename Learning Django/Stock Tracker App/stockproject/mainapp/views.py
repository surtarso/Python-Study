from django.shortcuts import render
#multithreading
import queue
from threading import Thread
from time import time
#error handling
from django.http import HttpResponse
#stocks info
from yahoo_fin.stock_info import *  #data for tables
import yfinance as yf   #data for graphs
#graphs
import plotly.graph_objs as go



# Create your views here.

## adds the stockpicker multi-click ui
def stockPicker(request):
    #escolhe o mercado: (yahoo-fin docs)
    stock_picker = tickers_ibovespa()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})
    

## adds the table of stocks
#recebe o submit ou do menu ou do searchbar
def stockTracker(request):
    #pega o resquest (ativo(s)) de name='stockpicker' (searchbar e menu)
    stockpicker = request.GET.getlist('stockpicker')
    print("request recebido em stockPicker:", stockpicker)

    #cria um dicionario para os papeis escolhidos
    data = {}
    #checa com os papeis do ibovespa
    available_stocks = tickers_ibovespa()

    #errorcheck
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Ocorreu um erro.")
    
    #teste multithreading
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time()

    #adiciona os papeis escolhidos para a tabela (single thread)
    # for i in stockpicker:
    #     #scrape yahoo data
    #     result = get_quote_table(i+'.SA')  ##.SA needed for B3!!
    #     data.update({i: result})

    #adiciona os papeis escolhidos para a tabela (multi thread)
    for i in range(n_threads):
        thread = Thread(
            target = lambda q,
            arg1: q.put({stockpicker[i]: get_quote_table(arg1+'.SA')}),
            args = (que, stockpicker[i])
            )
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()
    #update value
    while not que.empty():
        result = que.get()
        data.update(result)
    #time taken for get_quote_table() operations
    end = time()
    time_taken = end - start
    print(time_taken)
    #prints data and send to the browser
    print(data)
    return render(request, 'mainapp/stocktracker.html', {'data': data})



##-------------------------------is this a view?!?
def iniciaOperacao(request):
    print("passei por aqui...")
    useremail = request.GET.get('user_email')
    ativo = request.GET.get('ABEV3')
    compra = request.GET.get('preco_compra')
    venda = request.GET.get('preco_venda')
    periodobusca = request.GET.get('periodo_busca')
    tempoperacao = request.GET.get('tempo_operacao')




    return render(request, '', {})








###-------------------------------------------GRAFICOS:
def configGraph(request):
    data = yf.Ticker("ITSA4.SA").history("max")

    # ticker = request.GET.get("stockgraph")
    # print("request recebido em configGraph:", ticker)
    # data = yf.Ticker(ticker+".SA").history("max")

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x = data.index,
        open = data['Open'],
        high = data['High'],
        low = data['Low'],
        close = data['Close'],
        name = 'market data'
        ))

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1d', step='day', stepmode='backward'),
                dict(count=7, label='1wk', step='day', stepmode='backward'),
                dict(count=14, label='2wk', step='day', stepmode='backward'),
                dict(count=1, label='1mo', step='month', stepmode='backward'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(step='all')
                ])
        )
    )

    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, 'mainapp/graph.html', {'graph': graph})