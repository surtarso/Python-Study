
from django.urls import path
from . import views


urlpatterns = [
    
    #login page
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
]