from django.shortcuts import redirect, render
#multithreading
import queue
from threading import Thread
#error handling
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
#stocks info
from yahoo_fin.stock_info import *  #data for tables
import yfinance as yf   #data for graphs
#graphs
import plotly.graph_objs as go
#log in/ou register
from django.contrib.auth.decorators import login_required
from mainapp.forms import CarteiraForm
#models
from mainapp.models import Ativo, Mercado, CarteiraAtivo





## ------------------------------------------------------STOCK PICKER:
@login_required(login_url='login')
def stockPicker(request, pk):

    try:
        mercado = Mercado.objects.get(name=pk)
    except ObjectDoesNotExist:
        # return HttpResponse('no valid market chosen')
        return redirect('/')
    
    stock_picker = mercado.ativo_set.all()
    
    contexto = {'stockpicker':stock_picker, 'mercado':pk}
    return render(request, 'mainapp/stocks/stockpicker.html', contexto)



##------------------------------------------------------STOCK TRACKER:
#recebe o submit ou do stockpicker ou do searchbar
@login_required(login_url='login')
def stockTracker(request):
    
    #pega o resquest (ativo(s)) de name='stockpicker' (searchbar e menu)
    if request is not None:
        stockpicker = request.GET.getlist('stockpicker')

    #filter valid tickers
    valid_tickers = []
    mercados = Mercado.objects.all()
    # iterate trhu ALL tickers available in DB
    for mercado in mercados:
        ativos = mercado.ativo_set.all()
        for ativo in ativos:
            if str(ativo) in stockpicker:
                valid_tickers.append(str(ativo))
    
    #se entrar em stockpicker sem tickers validos
    if valid_tickers == []:
        return HttpResponse('ticker not found or list is empty')
        # return redirect('/')
    
    #multithreading
    n_threads = len(valid_tickers)
    thread_list = []
    que = queue.Queue()

    #cria um dicionario para os papeis escolhidos
    data = {}

    #adiciona os papeis escolhidos para a tabela (single thread)
    # for i in valid_tickers:
    #     #scrape yahoo data
    #     result = get_quote_table(i+'.SA')  ##.SA needed for B3!!
    #     data.update({i: result})

    #adiciona os papeis escolhidos para a tabela (multi thread)
    for i in range(n_threads):
        
        thread = Thread(
            target = lambda q,
            arg1: q.put({valid_tickers[i]: get_quote_table(str(arg1)+'.SA')}),
            args = (que, valid_tickers[i])
            )

        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()
        
    #update value
    while not que.empty():   
        result = que.get()
        data.update(result)


    contexto = {'data':data, 'room_name':'track'}
    return render(request, 'mainapp/stocks/stocktracker.html', contexto)


##------------------------------------------------------GRAFICOS:
@login_required(login_url='login')
def configGraph(request):

    if request.method == 'GET':

        ticker = request.GET.get('graph')
        data = yf.Ticker(str(ticker)+".SA").history("max")

        if data.empty:
            # return HttpResponse('invalid ticker or empty data frame')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

        graph = fig.to_html(full_html=True, default_height=600, default_width=810)
        
        contexto = {'graph': graph, 'ticker':ticker}
        return render(request, 'mainapp/stocks/graph.html', contexto)
    else:
        return HttpResponse('bad request')



##----------------------------------------------- CARTEIRA ATIVOS:
@login_required(login_url='login')
def showCarteira(request):
    data = {}
    carteiras = CarteiraAtivo.objects.all()
    carteira_usuario = []

    # pega apensas ativos do usuario atual!
    for ativo in carteiras:
        if ativo.user == request.user:
            carteira_usuario.append(ativo)
    
    # numero de threads de acordo com o numero de ativos do usuario
    n_threads = len(carteira_usuario)  
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        thread = Thread(
            target = lambda q,
            arg1: q.put({carteira_usuario[i]: get_quote_table(str(arg1)+'.SA')}),
            args = (que, carteira_usuario[i])
            )
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    #update value
    while not que.empty():
        result = que.get()
        data.update(result)

    contexto = {'data':data}
    return render(request, 'mainapp/stocks/carteira.html', contexto)



##-----------------------------------------------------CREATE ATIVO CARTEIRA:
@login_required(login_url='login')
def createCarteira(request):
    #get class reference
    form = CarteiraForm()
    #standard form on the POST method
    if request.method == 'POST':  #get that data
        form = CarteiraForm(request.POST)
        if form.is_valid():
            #create an instance
            carteira = form.save(commit=False)
            #a user will be added based on whos logged in
            carteira.user = request.user  #set the host
            carteira.save()  #save it
            return redirect('carteira') 

    contexto = {'carteira_form':form}
    return render(request, 'mainapp/stocks/carteira_form.html', contexto)



##------------------------------------------------------UPDATE ATIVO CARTEIRA:
@login_required(login_url='login')
def updateCarteira(request, pk):
    carteira = CarteiraAtivo.objects.get(id=pk)
    form = CarteiraForm(instance=carteira)

    #prevents logged in users to alter other users things
    if request.user != carteira.user:
        return HttpResponse("you are not allowed here")

    if request.method == 'POST':
        form = CarteiraForm(request.POST, instance=carteira)
        if form.is_valid():
            form.save()
            return redirect('carteira')

    contexto = {'carteira_form':form}
    return render(request, 'mainapp/stocks/carteira_form.html', contexto)


##------------------------------------------------------DELETE ATIVO CARTEIRA:
@login_required(login_url='login')
def deleteCarteira(request, pk):
    carteira = CarteiraAtivo.objects.get(id=pk)

    #prevents logged in users to delete other users things
    if request.user != carteira.user:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        carteira.delete()
        return redirect('carteira')

    return render(request, 'mainapp/basic_delete.html', { 'obj':carteira })