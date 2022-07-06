from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
#log in/ou register
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#models
from mainapp.models import Alerta, Mercado, Topic
from mainapp.forms import SignUpForm


## --------------------------------------------------------LOGIN:
def loginPage(request):
    """
    Autentica o login de usuarios e redireciona usuarios
    logados para a pagina de forums.
    Args:
        request (POST): username + password
    Returns:
        template: login_register.html
    """
    
    page = 'login'
    # redireciona usuarios logados para a pagina FORUM
    if request.user.is_authenticated:
        return redirect('forum')

    if request.method == 'POST':
        #get user name and password
        #values sent from submit button
        username = request.POST.get('username') #.lower()
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

    template = 'mainapp/users/login_register.html'
    context = {'page':page}
    return render(request, template, context)


##-------------------------------------------------------LOGOUT:
def logoutUser(request):
    """
    Desloga usuarios.
    Returns:
        redirect: home.html
    """
    logout(request)
    return redirect('/')


##------------------------------------------------------REGISTER:
def registerPage(request):
    """
    Registra um novo usuario e redireciona para FORUM
    após estar logado
    Args:
        request (POST): username, password, email
    Returns:
        template: login_register.html
    """
    
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

    template = 'mainapp/users/login_register.html'
    context = {'form': form}
    return render(request, template, context)


##----------------------------------------------------USER PROFILE:
@login_required(login_url='login')
def userProfile(request, pk):
    """
    Mostra a pagina de profile contendo itens criados pelo usuario
    Args:
        pk: user ID
    Returns:
        template: profile.html
        context: user, rooms, messages, topics, alertas, mercados
    """
    
    try:
        user = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        # return HttpResponse('this profile does not exist')
        # return redirect('/')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'mainapp/404.html')
    
    rooms = user.room_set.all()  # modelname_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    alertas = Alerta.objects.all()
    mercado = Mercado.objects.all()

    template = 'mainapp/users/profile.html'
    context = {
        'user':user,
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics,
        'alertas':alertas,
        'mercado':mercado
        }
    return render(request, template, context)
