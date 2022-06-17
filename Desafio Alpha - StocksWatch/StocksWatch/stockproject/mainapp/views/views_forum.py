from django.shortcuts import render, redirect
from django.db.models import Q
#error handling
from django.http import HttpResponse
#log in/ou register
from django.contrib.auth.decorators import login_required
#models
from mainapp.models import Message, Room, Topic
from mainapp.forms import RoomForm





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

    return render(request, 'mainapp/forum/forum.html', contexto)


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

    return render(request, 'mainapp/forum/room.html', contexto)


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
    return render(request, 'mainapp/forum/room_form.html', contexto)


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
    return render(request, 'mainapp/forum/room_form.html', contexto)


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

    return render(request, 'mainapp/basic_delete.html', { 'obj':room })



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

    return render(request, 'mainapp/basic_delete.html', { 'obj':message })
