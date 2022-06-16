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
from .models import Alerta, Mercado, Message, Room, Topic  #, AlarmIbovespa
from .forms import RoomForm, AlertForm, SignUpForm
#iframe security (graph attempts...)
from django.views.decorators.clickjacking import xframe_options_exempt




## -HOME:
def home(request):
    return render(request, 'mainapp/home.html', {})


##---------------------------------START USER----------------------------------##

## --------------------------------------------------------LOGIN:
def loginPage(request):
    page = 'login'
    # redirect logged in users to home page
    if request.user.is_authenticated:
        return redirect('forum')

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
            return redirect('forum')
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
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #get user object
            user.username = user.username.lower()
            user.save()
            login(request, user) #log the user
            return redirect('forum')
        else:
            messages.error(request, "registration error")

    return render(request, 'mainapp/login_register.html', {'form': form})


##----------------------------------------------------USER PROFILE:
@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()  # modelname_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    alerta = Alerta.objects.all()
    contexto = {
        'user':user,
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics,
        'alerta':alerta
        }
    return render(request, 'mainapp/profile.html', contexto)
##-------------------------------------END USER---------------------------------##



##-----------------------------------START FORUM--------------------------------##

##--------------------------------------------------------FORUM:
@login_required(login_url='login')
def forum(request):
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

    return render(request, 'mainapp/forum.html', contexto)


##---------------------------------------------------------ROOM:
@login_required(login_url='login')
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
            return redirect('forum')

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
##------------------------------------END FORUM--------------------------------##



##----------------------------------START ALERTS-------------------------------##

##------------------------------------------------------ALERT LIST:
@login_required(login_url='login')
def alerts(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    alerta = Alerta.objects.filter(
        Q(mercado__name__icontains=q) |
        Q(ativo__icontains=q)
        )

    mercado = Mercado.objects.all()
    alerta_count = alerta.count()

    contexto = { # itera em alerts.html
        'alerta': alerta,
        'mercado': mercado,
        'alerta_count':alerta_count,
        }

    return render(request, 'mainapp/alerts.html', contexto)


##------------------------------------------------------ALERT VIEW:
@login_required(login_url='login')
def alertView(request, pk):
    alert = Alerta.objects.get(id=pk)

    if request.method == 'POST': 
        return redirect('view-alert', pk=alert.id)

    contexto = {
        'alert':alert}
    return render(request, 'mainapp/alert_view.html', contexto)


##-----------------------------------------------------CREATE ALERT:
@login_required(login_url='login')
def createAlert(request):
    #get class reference
    form = AlertForm()
    #standard form on the POST method
    if request.method == 'POST':  #get that data
        form = AlertForm(request.POST)
        if form.is_valid():
            #create an instance of a room
            alert = form.save(commit=False)
            #a host will be added based on whos logged in
            alert.host = request.user  #set the host
            alert.save()  #save it
            return redirect('alerts')  ## MUDAR PARA LISTA DE ALERTAS DEPOIS

    contexto = {'alert_form':form}
    return render(request, 'mainapp/alert_form.html', contexto)



##------------------------------------------------------UPDATE ALERT:
@login_required(login_url='login')
def updateAlert(request, pk):
    alert = Alerta.objects.get(id=pk)
    form = AlertForm(instance=alert)

    #prevents logged in users to alter other users posts
    if request.user != alert.host:
        return HttpResponse("you are not allowed here")

    if request.method == 'POST':
        form = AlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect('alerts')

    contexto = {'alert_form':form}
    return render(request, 'mainapp/alert_form.html', contexto)



##------------------------------------------------------DELETE ALERT:
@login_required(login_url='login')
def deleteAlert(request, pk):
    alert = Alerta.objects.get(id=pk)

    #prevents logged in users to delete other users posts
    if request.user != alert.host:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        alert.delete()
        return redirect('alerts')

    return render(request, 'mainapp/delete.html', { 'obj':alert })
##--------------------------------END ALERTS-----------------------------------##



## ------------------------------------------------------STOCK PICKER:
@login_required(login_url='login')
def stockPicker(request):
    #popula a lista de mercado pelo yahoo-fin
    # stock_picker = tickers_ibovespa()
    stock_picker = ['ABEV3', 'AZUL4', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 
            'BEEF3', 'BPAC11', 'BRAP4', 'BRDT3', 'BRFS3', 'BRKM5', 'BRML3', 'BTOW3', 
            'CCRO3', 'CIEL3', 'CMIG4', 'COGN3', 'CPFE3', 'CRFB3', 'CSAN3', 'CSNA3', 
            'CVCB3', 'CYRE3', 'ECOR3', 'EGIE3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 
            'ENGI11', 'EQTL3', 'FLRY3', 'GGBR4', 'GNDI3', 'GOAU4', 'GOLL4', 'HAPV3', 
            'HGTX3', 'HYPE3', 'IGTA3', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 
            'LAME4', 'LREN3', 'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3', 'PCAR3', 
            'PETR3', 'PETR4', 'QUAL3', 'RADL3', 'RAIL3', 'RENT3', 'SANB11', 'SBSP3', 
            'SULA11', 'SUZB3', 'TAEE11', 'TIMP3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 
            'VIVT4', 'VVAR3', 'WEGE3', 'YDUQ3']
    
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})



##------------------------------------------------------STOCK TRACKER:
#recebe o submit ou do menu ou do searchbar
def stockTracker(request):
    #pega o resquest (ativo(s)) de name='stockpicker' (searchbar e menu)
    stockpicker = request.GET.getlist('stockpicker')
    print("Request recebido em stockTracker:", stockpicker)

    #cria um dicionario para os papeis escolhidos
    data = {}
    #checa com os papeis do ibovespa (yahoo-fin)
    # available_stocks = tickers_ibovespa()
    available_stocks = ['ABEV3', 'AZUL4', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 
            'BEEF3', 'BPAC11', 'BRAP4', 'BRDT3', 'BRFS3', 'BRKM5', 'BRML3', 'BTOW3', 
            'CCRO3', 'CIEL3', 'CMIG4', 'COGN3', 'CPFE3', 'CRFB3', 'CSAN3', 'CSNA3', 
            'CVCB3', 'CYRE3', 'ECOR3', 'EGIE3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 
            'ENGI11', 'EQTL3', 'FLRY3', 'GGBR4', 'GNDI3', 'GOAU4', 'GOLL4', 'HAPV3', 
            'HGTX3', 'HYPE3', 'IGTA3', 'IRBR3', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 
            'LAME4', 'LREN3', 'MGLU3', 'MRFG3', 'MRVE3', 'MULT3', 'NTCO3', 'PCAR3', 
            'PETR3', 'PETR4', 'QUAL3', 'RADL3', 'RAIL3', 'RENT3', 'SANB11', 'SBSP3', 
            'SULA11', 'SUZB3', 'TAEE11', 'TIMP3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 
            'VIVT4', 'VVAR3', 'WEGE3', 'YDUQ3']

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

##------------------------- END OF FILE ---------------------------------##

















########-------------------WIP-------------------------########
##---------------------------------------------------GRAFICOS:
@xframe_options_exempt  ## ok to load in iframe
def configGraph(request):
    print("REQUEST chegou em configGraph! : ", request)

    if request.method == 'GET' and request != None:
        
        ticker = request.GET.get('graph')
        print("DEVERIA SER UM TICKER: -->", ticker)
        # data = yf.Ticker(ticker+".SA").history("max")
        data = yf.Ticker("ITSA4.SA").history("max")

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
        return render(request, 'mainapp/fixlater/graph.html', {'graph': graph})
    else:
        return HttpResponse('Eu deveria ser um gráfico')
