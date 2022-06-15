from django.http import HttpResponse
from django.shortcuts import render
from .forms import AlertForm


##-------------------------------------------FORMULARIO PARA ALERTAS:
def alertForm(chamado):
    # gera um novo formulario baseado em forms.py
    alertform = AlertForm()

    # "alert_form" pode ser usado em alertform.html
    contexto = {"alert_form":alertform} 
    return render(chamado, 'main/alertform.html', contexto)