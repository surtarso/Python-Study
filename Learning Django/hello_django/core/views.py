## processa e retorna para o cliente
## pega requisicao, processa e manda uma resposta

from django.shortcuts import render, HttpResponse

# Create your views here.


def hello(request, nome, idade): ## informados pelo urls.py
    return HttpResponse('<h1>Hello {} de {} anos</h1>'.format(nome, idade))