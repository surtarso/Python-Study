from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mainapp.views import *
# from mainapp.views.views_home import home
# from mainapp.views.views_user import loginPage, logoutUser, registerPage, userProfile
# from mainapp.views.views_forum import forum, room, createRoom, updateRoom, deleteRoom, deleteMessage
# from mainapp.views.views_alert import alerts, alertView, createAlert, updateAlert, deleteAlert
# from mainapp.views.views_stocks import stockPicker, stockTracker, configGraph, showCarteira, createCarteira, updateCarteira, deleteCarteira

class TestURLs(SimpleTestCase):

    ##---------------------------------------------VIEWS_HOME
    def test_views_home_url_is_resolved(self):
        """
        Testa se o reverse de HOME existe e está correlacionado
        com seu template
        """
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)
        self.assertTemplateUsed('mainapp/home.html')

    ##----------------------------------------------VIEWS_USER
    def test_views_user_url_is_resolved(self):
        """
        Testa se o reverse de LOGIN existe e está correlacionado
        com seu template
        """
        url = reverse('login')
        self.assertEquals(resolve(url).func, loginPage)
        self.assertTemplateUsed('mainapp/users/login_register.html')

        """
        Testa se o reverse de LOGOUT existe e está correlacionado
        com seu template
        """
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

        """
        Testa se o reverse de REGISTER existe e está correlacionado
        com seu template
        """
        url = reverse('register')
        self.assertEquals(resolve(url).func, registerPage)
        self.assertTemplateUsed('mainapp/users/login_register.html')

        """
        Testa se o reverse de USER-PROFILE existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('user-profile', args=['pk'])
        self.assertEquals(resolve(url).func, userProfile)
        self.assertTemplateUsed('mainapp/users/profile.html')

    ##----------------------------------------------VIEWS_FORUM
    def test_views_forum_url_is_resolved(self):
        """
        Testa se o reverse de FORUM existe e está correlacionado
        com seu template
        """
        url = reverse('forum')
        self.assertEquals(resolve(url).func, forum)
        self.assertTemplateUsed('mainapp/forum/forum.html')

        """
        Testa se o reverse de ROOM existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('room', args=['pk'])
        self.assertEquals(resolve(url).func, room)
        self.assertTemplateUsed('mainapp/forum/room.html')

        """
        Testa se o reverse de CREATE-ROOM existe e está correlacionado
        com seu template
        """
        url = reverse('create-room')
        self.assertEquals(resolve(url).func, createRoom)
        self.assertTemplateUsed('mainapp/forum/room_form.html')

        """
        Testa se o reverse de UPDATE-ROOM existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('update-room', args=['pk'])
        self.assertEquals(resolve(url).func, updateRoom)
        self.assertTemplateUsed('mainapp/forum/room_form.html')

        """
        Testa se o reverse de DELETE-ROOM existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('delete-room', args=['pk'])
        self.assertEquals(resolve(url).func, deleteRoom)
        self.assertTemplateUsed('mainapp/basic_delete.html')

        """
        Testa se o reverse de DELETE-MESSAGE existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('delete-message', args=['pk'])
        self.assertEquals(resolve(url).func, deleteMessage)
        self.assertTemplateUsed('mainapp/basic_delete.html')

    ##----------------------------------------------VIEWS_ALERT
    def test_views_alert_url_is_resolved(self):
        """
        Testa se o reverse de ALERTS existe e está correlacionado
        com seu template
        """
        url = reverse('alerts')
        self.assertEquals(resolve(url).func, alerts)
        self.assertTemplateUsed('mainapp/stocks/alerts.html')

        """
        Testa se o reverse de VIEW-ALERT existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('view-alert', args=['pk'])
        self.assertEquals(resolve(url).func, alertView)
        self.assertTemplateUsed('mainapp/stocks/alert_view.html')

        """
        Testa se o reverse de CREATE-ALERTS existe e está correlacionado
        com seu template
        """
        url = reverse('create-alert')
        self.assertEquals(resolve(url).func, createAlert)
        self.assertTemplateUsed('mainapp/stocks/alert_form.html')

        """
        Testa se o reverse de UPDATE-ALERT existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('update-alert', args=['pk'])
        self.assertEquals(resolve(url).func, updateAlert)
        self.assertTemplateUsed('mainapp/stocks/alert_form.html')
        
        """
        Testa se o reverse de DELETE-ALERT existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('delete-alert', args=['pk'])
        self.assertEquals(resolve(url).func, deleteAlert)
        self.assertTemplateUsed('mainapp/basic_delete.html')

    ##-----------------------------------------------VIEWS_STOCKS
    def test_views_stocks_url_is_resolved(self):
        """
        Testa se o reverse de STOCKPICKER existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('stockpicker', args=['pk'])
        self.assertEquals(resolve(url).func, stockPicker)
        self.assertTemplateUsed('mainapp/stocks/stockpicker.html')

        """
        Testa se o reverse de STOCKTRACKER existe e está correlacionado
        com seu template
        """
        url = reverse('stocktracker')
        self.assertEquals(resolve(url).func, stockTracker)
        self.assertTemplateUsed('mainapp/stocks/stocktracker.html')

        """
        Testa se o reverse de GRAPH existe e está correlacionado
        com seu template
        """
        url = reverse('graph')
        self.assertEquals(resolve(url).func, configGraph)
        self.assertTemplateUsed('mainapp/stocks/graph.html')

        """
        Testa se o reverse de CARTEIRA existe e está correlacionado
        com seu template
        """
        url = reverse('carteira')
        self.assertEquals(resolve(url).func, showCarteira)
        self.assertTemplateUsed('mainapp/stocks/carteira.html')

        """
        Testa se o reverse de CREATE-CARTEIRA existe e está correlacionado
        com seu template
        """
        url = reverse('create-carteira')
        self.assertEquals(resolve(url).func, createCarteira)
        self.assertTemplateUsed('mainapp/stocks/carteira_form.html')

        """
        Testa se o reverse de UPDATE-CARTEIRA existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('update-carteira', args=['pk'])
        self.assertEquals(resolve(url).func, updateCarteira)
        self.assertTemplateUsed('mainapp/stocks/carteira_form.html')

        """
        Testa se o reverse de DELETE-CARTEIRA existe e está correlacionado
        com seu template, utilizando uma ID como argumento
        """
        url = reverse('delete-carteira', args=['pk'])
        self.assertEquals(resolve(url).func, deleteCarteira)
        self.assertTemplateUsed('mainapp/basic_delete.html')