from django.forms import ModelForm
from .models import CarteiraAtivo, Room, Alerta
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
        labels = {
            'topic': 'Assunto',
            'name': 'Título',
            'description': 'Conteudo'
        }

##--------------------------------FORMULARIO ALERTA:
class AlertForm(ModelForm):
    class Meta:
        model = Alerta
        fields = '__all__'
        exclude = ['host']
        labels = {
            'email': 'E-Mail para Alerta',
            'ativo': 'Ticker',
            'compra': 'Preço de Compra',
            'venda': 'Preço de Venda',
            'periodo': 'Minutos entre buscas',
            'duracao': 'Dias de operação'
        }

##--------------------------------FORMULARIO CARTEIRA:
class CarteiraForm(ModelForm):
    class Meta:
        model = CarteiraAtivo
        fields = '__all__'
        exclude = ['user']
        labels = {
            'ativo': 'Ticker',
            'preco_medio': 'Preço Médio',
            'quantidade': 'Total de Papeis',
            'nota': 'Peso na Carteira'
        }
