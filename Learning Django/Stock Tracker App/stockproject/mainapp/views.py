from django.shortcuts import render
#multithreading
import queue
from threading import Thread
from time import time
#error handling
from django.http import HttpResponse
#stocks info
from yahoo_fin.stock_info import *


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
    print(stockpicker)

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