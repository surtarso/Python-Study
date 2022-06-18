from django.forms import ModelForm
from .models import Room, Alerta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from yahoo_fin.stock_info import *


##------------------------------REGISTER FORM:
class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


##-------------------------------ROOM CREATE MESSAGE:
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

##--------------------------------FORMULARIO ALERTA:
class AlertForm(ModelForm):
    class Meta:
        model = Alerta
        fields = '__all__'
        exclude = ['host']
        