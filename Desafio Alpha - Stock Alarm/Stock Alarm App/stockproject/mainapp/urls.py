from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    #----- FAVICON
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('mainapp/images/favicon.ico'))),

    #----- HOME
    path('', views.home, name="home"),

    #----- USER
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    #----- FORUM
    path('forum/', views.forum, name="forum"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    #----- ALERTS
    path('create-alert/', views.createAlert, name="create-alert"),
    path('update-alert/<str:pk>/', views.updateAlert, name="update-alert"),
    path('delete-alert/<str:pk>/', views.deleteAlert, name="delete-alert"),

    #----- STOCKS (picker/tracker)
    path('stockpicker', views.stockPicker, name='stockpicker'),
    path('stocktracker', views.stockTracker, name='stocktracker'),



    ##WIP
    #path('graph', views.configGraph, name='graph'),
    #path('alarm-ibov', views.iniciaOperacao, name='alarm-ibov'),
]