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
#log in/ou register
from django.contrib.auth.decorators import login_required
#models
from mainapp.models import Mercado





## ------------------------------------------------------STOCK PICKER:
@login_required(login_url='login')
def stockPicker(request):

    mercado = Mercado.objects.get(name="IBOV")
    stock_picker = mercado.ativo_set.all()
    
    return render(request, 'mainapp/stocks/stockpicker.html', {'stockpicker':stock_picker})



##------------------------------------------------------STOCK TRACKER:
#recebe o submit ou do stockpicker ou do searchbar
def stockTracker(request):
    #pega o resquest (ativo(s)) de name='stockpicker' (searchbar e menu)
    stockpicker = request.GET.getlist('stockpicker')
    #cria um dicionario para os papeis escolhidos
    data = {}
    #checa com os papeis existentes do ibovespa (yahoo-fin)
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
    return render(request, 'mainapp/stocks/stocktracker.html', {'data': data})



##------------------------------------------------------GRAFICOS:
def configGraph(request):

    if request.method == 'GET' and request is not None:
        ticker = request.GET.get('graph')
        data = yf.Ticker(ticker+".SA").history("max")

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

        graph = fig.to_html(full_html=True, default_height=500, default_width=700)
        # graph = fig.show()
        return render(request, 'mainapp/stocks/graph.html', {'graph': graph})
    else:
        return HttpResponse('Eu deveria ser um gráfico')
