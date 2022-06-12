from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Message, Room, Topic
from .forms import RoomForm


# Create your views here.

##-----------------------------------------------------LOGIN:
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
    return render(request, 'base/login_register.html', contexto)


##-----------------------------------------------------LOGOUT:
def logoutUser(request):
    logout(request)
    return redirect('home')


##-----------------------------------------------------REGISTER:
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

    return render(request, 'base/login_register.html', {'form': form})


##-------------------------------------------------------HOME:
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

    return render(request, 'base/home.html', contexto)


##-------------------------------------------------------ROOM:
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

    return render(request, 'base/room.html', contexto)


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
    return render(request, 'base/profile.html', contexto)


##----------------------------------------------------CREATE ROOM:
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
    return render(request, 'base/room_form.html', contexto)


##----------------------------------------------------UPDATE ROOM:
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
    return render(request, 'base/room_form.html', contexto)


##----------------------------------------------------DELETE ROOM:
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    #prevents logged in users to delete other users posts
    if request.user != room.host:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', { 'obj':room })



##---------------------------------------------------DELETE MESSAGES:
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    #prevents logged in users to delete other users messages
    if request.user != message.user:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', { 'obj':message })