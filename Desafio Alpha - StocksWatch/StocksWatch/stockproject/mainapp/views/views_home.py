from django.shortcuts import render


## -------------------------------------------------------HOME:
def home(request):
    return render(request, 'mainapp/home.html')