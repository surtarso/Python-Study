from django.shortcuts import render, redirect
from django.db.models import Q
#error handling
from django.http import HttpResponse
#log in/ou register
from django.contrib.auth.decorators import login_required
#models
from mainapp.models import Alerta, Mercado
from mainapp.forms import AlertForm



##------------------------------------------------------ALERT LIST:
@login_required(login_url='login')
def alerts(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    alerta = Alerta.objects.filter(
        Q(mercado__name__icontains=q) |
        Q(ativo__ticker__icontains=q)
        )

    mercado = Mercado.objects.all()
    alerta_count = alerta.count()
    alertas = Alerta.objects.filter(Q(ativo__ticker__icontains=q))

    contexto = { # itera em alerts.html
        'alerta': alerta,
        'alertas': alertas,
        'mercado': mercado,
        'alerta_count':alerta_count,
        }

    return render(request, 'mainapp/stocks/alerts.html', contexto)


##------------------------------------------------------ALERT VIEW:
@login_required(login_url='login')
def alertView(request, pk):
    alert = Alerta.objects.get(id=pk)

    if request.method == 'POST': 
        return redirect('view-alert', pk=alert.id)

    contexto = {'alert':alert}
    return render(request, 'mainapp/stocks/alert_view.html', contexto)


##-----------------------------------------------------CREATE ALERT:
@login_required(login_url='login')
def createAlert(request):
    #get class reference
    form = AlertForm()
    #standard form on the POST method
    if request.method == 'POST':  #get that data
        form = AlertForm(request.POST)
        if form.is_valid():
            #create an instance of an alert
            alert = form.save(commit=False)
            #a host will be added based on whos logged in
            alert.host = request.user  #set the host
            alert.save()  #save it
            return redirect('alerts')  ## MUDAR PARA LISTA DE ALERTAS DEPOIS

    contexto = {'alert_form':form}
    return render(request, 'mainapp/stocks/alert_form.html', contexto)



##------------------------------------------------------UPDATE ALERT:
@login_required(login_url='login')
def updateAlert(request, pk):
    alert = Alerta.objects.get(id=pk)
    form = AlertForm(instance=alert)

    #prevents logged in users to alter other users posts
    if request.user != alert.host:
        return HttpResponse("you are not allowed here")

    if request.method == 'POST':
        form = AlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect('alerts')

    contexto = {'alert_form':form}
    return render(request, 'mainapp/stocks/alert_form.html', contexto)



##------------------------------------------------------DELETE ALERT:
@login_required(login_url='login')
def deleteAlert(request, pk):
    alert = Alerta.objects.get(id=pk)

    #prevents logged in users to delete other users posts
    if request.user != alert.host:
        return HttpResponse("it does not belong to you")

    if request.method == 'POST':
        alert.delete()
        return redirect('alerts')

    return render(request, 'mainapp/basic_delete.html', { 'obj':alert })
