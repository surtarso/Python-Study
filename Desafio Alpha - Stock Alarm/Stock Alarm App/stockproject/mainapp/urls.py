from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.stockPicker, name='stockpicker'),

    path('stocktracker', views.stockTracker, name='stocktracker'),

    path('graph', views.configGraph, name='stockgraph'),

    # path('alertoperation', views.iniciaOperacao, name='alertoperation'),
]