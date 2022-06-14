from django.shortcuts import render, redirect
from django.db.models import Q
#multithreading
import queue
from threading import Thread
from time import time, sleep
#error handling
from django.http import HttpResponse
from django.contrib import messages
#stocks info
from yahoo_fin.stock_info import *  #data for tables
import yfinance as yf   #data for graphs
#graphs
import plotly.graph_objs as go
#log in/ou register
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
#models
from .models import Message, Room, Topic
from .forms import RoomForm



# Create your views here.

## -----------------------------------------------------LOGIN:
def loginPage(request):
    page = 'login'
    # redirect logged in users to home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        #get user name and password
        #values sent from the front-end
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #check if user exists in db
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user or pass does not exist")

        #this creates a 'user' Object w/ username/password
        user = authenticate(request, username=username, password=password)
        # is the user logged in correctly
        if user is not None:
            #create a login session
            login(request, user)
            #redirect the user
            return redirect('home')
        else:
            #send error message
            messages.error(request, "user or pass does not exist")

    contexto = {'page':page}
    return render(request, 'mainapp/login_register.html', contexto)


##-------------------------------------------------------LOGOUT:
def logoutUser(request):
    logout(request)
    return redirect('home')


##------------------------------------------------------REGISTER:
def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #get user object
            user.username = user.username.lower()
            user.save()
            login(request, user) #log the user
            return redirect('home')
        else:
            messages.error(request, "registration error")

    return render(request, 'mainapp/login_register.html', {'form': form})


##--------------------------------------------------------HOME:
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    room_count = rooms.count()
    # filters to see only topic related messages on right sidebar
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    contexto = { # itera em home.html
        'rooms': rooms,
        'topics': topics,
        'room_count':room_count,
        'room_messages':room_messages
        }

    return render(request, 'mainapp/home.html', contexto)


##---------------------------------------------------------ROOM:
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        ) 
        #add user to manytomany field
        room.participants.add(request.user) 
        return redirect('room', pk=room.id)

    contexto = {
        'room':room,
        'room_messages':room_messages,
        'participants':participants
        }

    return render(request, 'mainapp/room.html', contexto)


##----------------------------------------------------USER PROFILE:
@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()  # modelname_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    contexto = {
        'user':user,
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics
        }
    return render(request, 'mainapp/profile.html', contexto)


##-----------------------------------------------------CREATE ROOM:
@login_required(login_url='login')
def createRoom(request):
    #get class reference
    form = RoomForm()
    #standard form on the POST method
    if request.method == 'POST':  #get that data
        form = RoomForm(request.POST)
        if form.is_valid():
            #create an instance of a room
            room = form.save(commit=False)
            #a host will be added based on whos logged in
            room.host = request.user  #set the host
            room.save()  #save it
            return redirect('home')

    contexto = {'form':form}
    return render(request, 'mainapp/room_form.html', contexto)


##------------------------------------------------------UPDATE ROOM:
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    #prevents logged in users to alter other users posts
    if request.user != room.host:
        return HttpResponse("you are not allowed here")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    contexto = {'form':form}
    return render(request, 'mainapp/room_form.html', contexto)


##------------------------------------------------------DELETE ROOM:
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    #prevents logged in users to delete other users posts
    if request.user != room.host:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'mainapp/delete.html', { 'obj':room })



##----------------------------------------------------DELETE MESSAGES:
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    #prevents logged in users to delete other users messages
    if request.user != message.user:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'mainapp/delete.html', { 'obj':message })



## ------------------------------------------------------STOCK PICKER:
@login_required(login_url='login')
def stockPicker(request):
    #popula a lista de mercado: (yahoo-fin docs)
    stock_picker = tickers_ibovespa()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})



##------------------------------------------------------STOCK TRACKER:
## adds the table of stocks
#recebe o submit ou do menu ou do searchbar
@login_required(login_url='login')
def stockTracker(request):
    #pega o resquest (ativo(s)) de name='stockpicker' (searchbar e menu)
    stockpicker = request.GET.getlist('stockpicker')
    print("request recebido em stockTracker:", stockpicker)

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



###---------------------------------------------------GRAFICOS:
def configGraph(request):
    data = yf.Ticker("ITSA4.SA").history("max")

    # ticker = request.GET.get("graph_ticker")
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




##---------------------------------is this a view?!?--LOGICA ALERTA:
# def iniciaOperacao(request):
#     print("request de iniciaOperacao: ", request)

#     #como recebo esses valores??
#     papel_in = request.POST.get('ABEV3.SA') #testando...
#     email_in = request.POST.get('user_email')
#     price_min = request.POST.get('preco_compra')
#     price_max = request.POST.get('preco_venda')
#     periodo_in = request.POST.get('periodo_busca')
#     dias_in = request.POST.get('tempo_operacao')

#     IS_DEBUG = True  # false for real time
#     DIA = 86400  # 1 dia em segundos

#     # formata a busca inserida
#     if IS_DEBUG:
#         periodo = periodo_in  # mantem em segundos para debug
#         dias = dias_in * 3  # mantem em um range aceitavel para debug
#     else:
#         periodo = periodo_in * 60  # formata o input para minutos
#         dias = dias_in * DIA  # formata o input para dias

#     ticker = yf.Ticker(papel_in.upper()+".SA") #formata para yahoo

#     # cria nova lista de cotacoes
#     cotacoes = []

#     i = 0
#     while i != dias:
#         #pega preço atual do ticker
#         cotacao = round(ticker.info['regularMarketPrice'], 2)
#         #insere preço no inicio da tabela
#         cotacoes.insert(0, cotacao)

#         #PLACEHOLDER: adicionar sistema de email
#         if cotacao >= price_max:
#             print("\nPreço de VENDA atingido---> enviado para:", email_in)
#         elif cotacao <= price_min:
#             print("\nPreço de COMPRA atingido---> enviado para:", email_in)
#         else:
#             pass
#         sleep(periodo)
#         i += 1

#     ## PLACEHOLDER: adicionar sistema de email
#     print("Enviando para", email_in, ":\n--> Dias de operação com", papel_in.upper(), "excedidos, faça uma nova operação.\n")
#     ## PLACEHOLDER: é para gerar uma tabela com esses valores
#     print("Historico de", dias_in, "dia(s) de operação com", papel_in.upper(),":\n", cotacoes)

#     ## I DONT WANT TO RENDER?? RETURN WHAT???
#     return render(request, '', {})