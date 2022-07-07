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
#models
from mainapp.models import Ativo, Mercado, CarteiraAtivo
from mainapp.forms import CarteiraForm




## ------------------------------------------------------STOCK PICKER:
@login_required(login_url='login')
def stockPicker(request, pk):
    """
    View para selecao de ativos para cotacoes. Recebe o nome do mercado
    para apresentar apensar os ativos pertencentes a tal mercado.
    Args:
        pk (String): nome do mercado
    Returns:
        template: stockpicker.html
        context: stockpicker (tickers) e mercados (nomes)
    """

    try:
        mercado = Mercado.objects.get(name=pk)
    except ObjectDoesNotExist:
        # return HttpResponse('no valid market chosen')
        # return redirect('/')
        return render(request, 'mainapp/404.html')
    
    stock_picker = mercado.ativo_set.all()
    
    template = 'mainapp/stocks/stockpicker.html'
    context = {'stockpicker':stock_picker, 'mercado':pk}
    return render(request, template, context)



##------------------------------------------------------STOCK TRACKER:
#recebe o submit ou do stockpicker ou do searchbar
@login_required(login_url='login')
def stockTracker(request):
    """
    Recebe de stockpicker os nomes dos ativos para pesquisa de precos
    Args:
        request (List): Lista de ativos selecionados para pesquisa de cotacao
    Returns:
        template: stocktracker.html
        context: lista de ativos, salas de atualizacao para celery
    """
    #pega o resquest (ativo(s)) de name='stockpicker' (searchbar e menu)
    if request is not None:
        stockpicker = request.GET.getlist('stockpicker')

    #filter valid tickers
    valid_tickers = []
    mercados = Mercado.objects.all()
    for mercado in mercados:
        ativos = mercado.ativo_set.all()
        # iterate trhu ALL tickers available in DB
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

    #cria um dicionario para o resultado dos papeis escolhidos
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

    template = 'mainapp/stocks/stocktracker.html'
    context = {'data':data, 'room_name':'track'}
    return render(request, template, context)


##------------------------------------------------------GRAFICOS:
@login_required(login_url='login')
def configGraph(request):
    """
    Mostra graficos (plotly) para o usuario do ativo escolhido
    Args:
        request (String): nome do ativo para mostrar grafico
    Returns:
        template: graph.html
        context: o grafico em si e o nome do ativo para o titulo
    """
    if request.method == 'GET':

        ticker = request.GET.get('ticker')
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
        
        template = 'mainapp/stocks/graph.html'
        context = {'graph': graph, 'ticker':ticker}
        return render(request, template, context)
    else:
        return HttpResponse('bad request')
    

##----------------------------------------------- CARTEIRA ATIVOS:
@login_required(login_url='login')
def showCarteira(request):
    """
    Carteira de ativos do usuario para acompanhamento e balanceamento.
    Returns:
        template: carteira.html
        context: ativos que o usuario selecionou para sua carteira
    """
    data = {}
    carteiras = CarteiraAtivo.objects.all()
    carteira_usuario = []
    figure_ativos = []
    figure_notas = []
    figure_markets = []

    # pega apensas ativos do usuario atual!
    for ativo in carteiras:
        if ativo.user == request.user:
            carteira_usuario.append(ativo)
            figure_ativos.append(str(ativo.ativo.ticker))
            figure_notas.append(int(ativo.nota))
            figure_markets.append(str(ativo.ativo.mercado))

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
    
    ##--------- pie chart - ativos --------------
    stocks_fig = go.Figure()
    stocks_fig.add_trace(go.Pie(
        labels = figure_ativos,
        values = figure_notas,
        direction ='counterclockwise',
        sort = True
        ))
    figure_s = stocks_fig.to_html(full_html = True)#, default_height=250, default_width=350)
    
    ##--------- pie chart - mercados ------------
    markets_fig = go.Figure()
    markets_fig.add_trace(go.Pie(
        labels = figure_markets,
        direction ='counterclockwise',
        sort = True
        ))
    figure_m = markets_fig.to_html(full_html = True, default_height=225, default_width=300)
    
    
    template = 'mainapp/stocks/carteira.html'
    context = {'data':data,
               'figure_stocks':figure_s,
               'figure_markets':figure_m}
    return render(request, template, context)



##-----------------------------------------------------CREATE ATIVO CARTEIRA:
@login_required(login_url='login')
def createCarteira(request):
    """
    Adiciona novos ativos para a carteira de balanceamento do usuario
    Returns:
        template: carteira_form.html
        context: formulario para adicao de ativo em carteira
    """
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

    template = 'mainapp/stocks/carteira_form.html'
    context = {'carteira_form':form}
    return render(request, template, context)



##------------------------------------------------------UPDATE ATIVO CARTEIRA:
@login_required(login_url='login')
def updateCarteira(request, pk):
    """
    Modifica informacoes do ativo adicionado em carteira
    Args:
        pk: ID do item a ser modificado
    Returns:
        template: carteira_form.html
        context: formulario de adicao de ativo ja preenchido
    """
    try:
        carteira = CarteiraAtivo.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, 'mainapp/404.html')
    form = CarteiraForm(instance=carteira)

    #prevents logged in users to alter other users things
    if request.user != carteira.user:
        return HttpResponse("you are not allowed here")

    if request.method == 'POST':
        form = CarteiraForm(request.POST, instance=carteira)
        if form.is_valid():
            form.save()
            return redirect('carteira')

    template = 'mainapp/stocks/carteira_form.html'
    context = {'carteira_form':form}
    return render(request, template, context)


##------------------------------------------------------DELETE ATIVO CARTEIRA:
@login_required(login_url='login')
def deleteCarteira(request, pk):
    """
    Apaga um ativo da carteira de balanceamento do usuario
    Args:
        pk: id do ativo a ser apagado
    Returns:
        template: basic_delete.html
        context: confirmacao do ativo a ser deletado
    """
    try:
        carteira = CarteiraAtivo.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, 'mainapp/404.html')

    #prevents logged in users to delete other users things
    if request.user != carteira.user:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        carteira.delete()
        return redirect('carteira')

    template = 'mainapp/basic_delete.html'
    context = {'obj':carteira}
    return render(request, template, context)