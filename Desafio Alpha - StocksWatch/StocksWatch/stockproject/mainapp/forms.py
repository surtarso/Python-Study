from django.forms import EmailInput, ModelForm, NumberInput, TextInput, Textarea
from .models import CarteiraAtivo, Room, Alerta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from yahoo_fin.stock_info import *


##------------------------------REGISTER FORM:
class SignUpForm(UserCreationForm):
    """
    Formulario para criacao de novo usuario
    """
    
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'max-width: 300px;'
            })
    )

    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'max-width: 300px;'
            })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nome',
            'email': 'E-Mail'
        }   
        widgets ={
            'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                })
        }


##-------------------------------ROOM CREATE MESSAGE:
class RoomForm(ModelForm):
    """
    Formulario para criacao/edicao de uma sala de bate papo

    """
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        labels = {
            'topic': 'Assunto',
            'name': 'Título',
            'description': 'Conteudo'
        }
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Adicione um título'
                }),
            'description': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                'placeholder': 'O que está pensando?'
                }),
        }

##--------------------------------FORMULARIO ALERTA:
class AlertForm(ModelForm):
    """
    Formulario para criacao/edicao de um alerta de precos
    """
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
        widgets = {
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'adicione@seu.email'
            }),
            'compra': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;'
            }),
            'venda': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;'
            }),
            'periodo': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;'
            }),
            'duracao': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;'
            })
        }

##--------------------------------FORMULARIO CARTEIRA:
class CarteiraForm(ModelForm):
    """
    Formulario para adicao/edicao de um novo ativo na
    carteira de balanceamento do usuario
    """
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
        widgets = {
            'preco_medio': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;'
            }),
            'quantidade': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;'
            }),
            'nota': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;'
            })
        }
