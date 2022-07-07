from django.shortcuts import render


## -------------------------------------------------------HOME:
def home(request):
    return render(request, 'mainapp/home.html')

def http_404_error(request, exception):
    return render(request, 'mainapp/404.html', status=404)