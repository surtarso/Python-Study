from django.http import HttpResponse
from django.shortcuts import render
from .forms import AlertForm

# Create your views here.

def home(response):
    alertform = AlertForm()

    contexto = {"alertform":alertform}
    return render(response, 'main/home.html', contexto)