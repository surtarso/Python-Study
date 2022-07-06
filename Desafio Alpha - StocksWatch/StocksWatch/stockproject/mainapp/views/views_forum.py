from django.core.exceptions import ObjectDoesNotExist
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
    """
    View onde o usuario acessa as salas de bate papo existentes
    Returns:
        template: forum.html
        context: rooms, topics, room_count, messages
    """
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

    template = 'mainapp/forum/forum.html'
    context = { # itera em home.html
        'rooms': rooms,
        'topics': topics,
        'room_count':room_count,
        'room_messages':room_messages
        }
    return render(request, template, context)


##-----------------------------------------------------VIEW ROOM:
@login_required(login_url='login')
def room(request, pk):
    """
    View para visualizar uma sala especifica
    Args:
        pk: room ID
    Returns:
        template: room.html
        context: room, messages, participants
    """
    try:
        room = Room.objects.get(id=pk)
    except ObjectDoesNotExist:
        # return HttpResponse('this room does not exist')
        # return redirect('forum')
        return render(request, 'mainapp/404.html')
    
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

    template = 'mainapp/forum/room.html'
    context = {
        'room':room,
        'room_messages':room_messages,
        'participants':participants
        }
    return render(request, template, context)


##-----------------------------------------------------CREATE ROOM:
@login_required(login_url='login')
def createRoom(request):
    """
    View responsavel pela criacao de novas salas de bate papo
    Returns:
        template: room_form.html
        context: formulario de criacao de sala
    """
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

    template = 'mainapp/forum/room_form.html'
    context = {'form':form}
    return render(request, template, context)


##------------------------------------------------------UPDATE ROOM:
@login_required(login_url='login')
def updateRoom(request, pk):
    """
    View para atualizacao de sala de bate papo
    Args:
        pk: room ID
    Returns:
        template: room_form.html
        context: formulario pré preenchido da sala
    """
    try:
        room = Room.objects.get(id=pk)
    except ObjectDoesNotExist:
        # return HttpResponse('this room does not exist')
        # return redirect('forum')
        return render(request, 'mainapp/404.html')
    
    form = RoomForm(instance=room)

    #prevents logged in users to alter other users posts
    if request.user != room.host:
        return HttpResponse("you are not allowed here")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('forum')

    template = 'mainapp/forum/room_form.html'
    context = {'form':form}
    return render(request, template, context)


##------------------------------------------------------DELETE ROOM:
@login_required(login_url='login')
def deleteRoom(request, pk):
    """
    View responsavel por apagar salas de bate papo
    Args:
        pk: room ID
    Returns:
        template: basic_delete.html
        context: sala a ser deletada
    """
    try:
        room = Room.objects.get(id=pk)
    except ObjectDoesNotExist:
        # return HttpResponse('this room does not exist')
        # return redirect('forum')
        return render(request, 'mainapp/404.html')

    #prevents logged in users to delete other users posts
    if request.user != room.host:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        room.delete()
        return redirect('forum')

    template = 'mainapp/basic_delete.html'
    context = {'obj':room}
    return render(request, template, context)



##----------------------------------------------------DELETE MESSAGES:
@login_required(login_url='login')
def deleteMessage(request, pk):
    """
    View responsavel por deletar mensagens contidas em salas de bate papo
    Args:
        pk: ID da mensagem
    Returns:
        template: basic_delete.html
        context: mensagem a ser apagada.
    """
    try:
        message = Message.objects.get(id=pk)
    except ObjectDoesNotExist:
        # return HttpResponse('this message does not exist')
        # return redirect('forum')
        return render(request, 'mainapp/404.html')
    
    #prevents logged in users to delete other users messages
    if request.user != message.user:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        message.delete()
        return redirect('forum')
    
    template = 'mainapp/basic_delete.html'
    context = {'obj':message}
    return render(request, template, context)
