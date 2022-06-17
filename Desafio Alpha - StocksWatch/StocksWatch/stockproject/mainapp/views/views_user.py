from django.shortcuts import render, redirect
from django.contrib import messages
#log in/ou register
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#models
from mainapp.models import Alerta, Topic
from mainapp.forms import SignUpForm



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
    return render(request, 'mainapp/users/login_register.html', contexto)


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

    return render(request, 'mainapp/users/login_register.html', {'form': form})


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
        'alertas':alerta
        }
    return render(request, 'mainapp/users/profile.html', contexto)
