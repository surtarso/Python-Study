from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    #favicon
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('mainapp/images/favicon.ico'))),

    #login related
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    #home folder (empty path)
    path('', views.home, name="home"),

    #rooms by ID
    path('room/<str:pk>/', views.room, name="room"),

    #user profile page by ID
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    #room page
    path('create-room/', views.createRoom, name="create-room"),

    #room manipulation by ID
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    #stockpicker
    path('stockpicker', views.stockPicker, name='stockpicker'),
    #stocktracker
    path('stocktracker', views.stockTracker, name='stocktracker'),



    ##WIP
    path('graph', views.configGraph, name='graph'),
    # path('aleta', views.iniciaOperacao, name='alerta'),
]