from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.models import Mercado
from .forms import AlertForm

"""
POST -> passa os dados com criptgrafia & faz modificacoes na database.
GET  -> pega a informacao e cola na URL & le a URL p/ pegar a informacao. (bla.com/search=?)
Default é sempre GET. POST tem que ser explicito.
"""

##-------------------------------------------FORMULARIO PARA ALERTAS:
def alertForm(chamado):
    # se as informacoes estiverem preenchidas: (clicou submit c/ POST)
    if chamado.method == 'POST':
        # cria um dicionation com as ids e valores entrados no site
        alertform = AlertForm(chamado.POST)

        # checa se o formulario esta valido:
        if alertform.is_valid():
            # pega os dados e desencripta usando as variaveis de alertform
            email = alertform.cleaned_data["email"]
            mercado = alertform.cleaned_data["mercado"]
            ativo = alertform.cleaned_data["ativo"]
            precocompra = alertform.cleaned_data["precocompra"]
            precovenda = alertform.cleaned_data["precovenda"]
            periodo = alertform.cleaned_data["periodo"]
            duracao = alertform.cleaned_data["duracao"]
            checkbox = alertform.cleaned_data["checkbox"]
            print("RECEBI:",email, mercado, ativo, precocompra, precovenda, periodo, duracao, checkbox)

            # # manda processar??
            # pedido = Mercado
            # # salva os dados??
            # pedido.save()

            # return HttpResponseRedirect("/%i" % pedido.id)
            return HttpResponse("Seu pedido foi enviado com sucesso.")

    else:  # acabou de entrar na pagina:
        # gera um novo formulario baseado em forms.py
        alertform = AlertForm()

    # "alert_form" pode ser usado em alertform.html
    contexto = {"alert_form":alertform} 
    return render(chamado, 'main/alertform.html', contexto)