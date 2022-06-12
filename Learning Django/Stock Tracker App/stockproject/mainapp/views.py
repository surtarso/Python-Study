from django.shortcuts import render
from yahoo_fin.stock_info import *


# Create your views here.

## adds the stockpicker multi-click ui
def stockPicker(request):
    stock_picker = tickers_ibovespa()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})

## adds the table of stocks
def stockTracker(request):
    return render(request, 'mainapp/stocktracker.html')