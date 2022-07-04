from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mainapp.views.views_home import home
from mainapp.views.views_user import loginPage, logoutUser, registerPage, userProfile
from mainapp.views.views_forum import forum, room, createRoom, updateRoom, deleteRoom, deleteMessage
from mainapp.views.views_alert import alerts, alertView, createAlert, updateAlert, deleteAlert
from mainapp.views.views_stocks import stockPicker, stockTracker, configGraph, showCarteira, createCarteira, updateCarteira, deleteCarteira

class TestURLs(SimpleTestCase):

    ##---------------------------------------------VIEWS_HOME
    def test_views_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    ##----------------------------------------------VIEWS_USER
    def test_views_user_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, loginPage)

        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

        url = reverse('register')
        self.assertEquals(resolve(url).func, registerPage)

        url = reverse('user-profile', args=['pk'])
        self.assertEquals(resolve(url).func, userProfile)

    ##----------------------------------------------VIEWS_FORUM
    def test_views_forum_url_is_resolved(self):
        url = reverse('forum')
        self.assertEquals(resolve(url).func, forum)

        url = reverse('room', args=['pk'])
        self.assertEquals(resolve(url).func, room)

        url = reverse('create-room')
        self.assertEquals(resolve(url).func, createRoom)

        url = reverse('update-room', args=['pk'])
        self.assertEquals(resolve(url).func, updateRoom)

        url = reverse('delete-room', args=['pk'])
        self.assertEquals(resolve(url).func, deleteRoom)

        url = reverse('delete-message', args=['pk'])
        self.assertEquals(resolve(url).func, deleteMessage)

    ##----------------------------------------------VIEWS_ALERT
    def test_views_alert_url_is_resolved(self):
        url = reverse('alerts')
        self.assertAlmostEquals(resolve(url).func, alerts)

        url = reverse('view-alert', args=['pk'])
        self.assertAlmostEquals(resolve(url).func, alertView)

        url = reverse('create-alert')
        self.assertAlmostEquals(resolve(url).func, createAlert)

        url = reverse('update-alert', args=['pk'])
        self.assertAlmostEquals(resolve(url).func, updateAlert)

        url = reverse('delete-alert', args=['pk'])
        self.assertAlmostEquals(resolve(url).func, deleteAlert)

    ##-----------------------------------------------VIEWS_STOCKS
    def test_views_stocks_url_is_resolved(self):
        url = reverse('stockpicker', args=['pk'])
        self.assertAlmostEquals(resolve(url).func, stockPicker)

        url = reverse('stocktracker')
        self.assertAlmostEquals(resolve(url).func, stockTracker)

        url = reverse('graph')
        self.assertAlmostEquals(resolve(url).func, configGraph)

        url = reverse('carteira')
        self.assertAlmostEquals(resolve(url).func, showCarteira)

        url = reverse('create-carteira')
        self.assertAlmostEquals(resolve(url).func, createCarteira)

        url = reverse('update-carteira', args=['pk'])
        self.assertAlmostEquals(resolve(url).func, updateCarteira)

        url = reverse('delete-carteira', args=['pk'])
        self.assertAlmostEquals(resolve(url).func, deleteCarteira)