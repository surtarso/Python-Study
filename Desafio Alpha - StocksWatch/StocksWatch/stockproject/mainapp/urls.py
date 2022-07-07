from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    #----- FAVICON
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('mainapp/images/favicon.ico'))),

    #----- HOME (views.views_home.py)
    path('', views.home, name="home"),

    #----- USER (views.views_user.py)
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    #----- FORUM (views.views_forum.py)
    path('forum/', views.forum, name="forum"),  # forums "home"
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    #----- ALERTS (views.views_alert.py)
    path('alerts/', views.alerts, name="alerts"),  # alerts "home"
    path('create-alert/', views.createAlert, name="create-alert"),
    path('update-alert/<str:pk>/', views.updateAlert, name="update-alert"),
    path('delete-alert/<str:pk>/', views.deleteAlert, name="delete-alert"),

    
    #----- STOCKS (views.views_stocks.py)
    path('stockpicker/<str:pk>', views.stockPicker, name='stockpicker'),
    path('stocktracker', views.stockTracker, name='stocktracker'),
    path('graph', views.configGraph, name="graph"),
    path('carteira', views.showCarteira, name="carteira"),
    path('create-carteira/', views.createCarteira, name="create-carteira"),
    path('update-carteira/<str:pk>/', views.updateCarteira, name="update-carteira"),
    path('delete-carteira/<str:pk>/', views.deleteCarteira, name="delete-carteira"),
]