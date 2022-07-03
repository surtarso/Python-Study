from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.

# class TrySomethingTest(TestCase):
#     def test_something(self):
#         self.assertTrue(1==1)
#         self.assertEqual(1,1)

User = get_user_model()
class TestLoggedInUserURLs(TestCase):
    #set up user
    def setUp(self):
        user_a_password = 'baddybald123'
        user_a = User(username='test', email='test@invalid.com')
        user_a.set_password(user_a_password)
        user_a.save()
        self.user_a_password = user_a_password
        self.user_a = user_a

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):
        user_a = User.objects.get(username='test')
        self.assertTrue(user_a.check_password(self.user_a_password))

    def test_login_redirect_url(self):
        login_page = '/login/'
        login_redirect = '/forum/'
        data = {'username': self.user_a.get_username(),
                'password': self.user_a_password}
        #go to login page and post data
        response = self.client.post(login_page, data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get('PATH_INFO')
        #test redirect from login to forums:
        self.assertEqual(redirect_path, login_redirect)
        self.assertEqual(status_code, 200)

    def test_logged_in_normal_user_access_admin_panel(self):
        self.client.login(username='test', password = self.user_a_password)
        self.assertTrue(self.user_a.is_authenticated)
        response = self.client.post('/admin/')
        #test normal user unable to enter admin panel:
        self.assertEqual(response.status_code, 302)

    def test_valid_urls_for_logged_in_users(self):
        self.client.login(username='test', password = self.user_a_password)
        self.assertTrue(self.user_a.is_authenticated)

        urls = ['/stockpicker/IBOV', '/stockpicker/IFIX', '/stocktracker',
                '/forum/', '/graph', '/alerts/', '/carteira']
        for url in urls:
            response = self.client.post(url, follow=True)
            self.assertEqual(response.status_code, 200)

        #test profile with ID
        response = self.client.get(reverse('user-profile', args=[self.user_a.pk]))
        self.assertEqual(response.status_code, 200)

class TestLoggedOutUserURLs(TestCase):
    
    def test_valid_urls_for_logged_out_users(self):
        urls = ['/', '/login/', '/register/']
        for url in urls:
            response = self.client.post(url)
            self.assertEqual(response.status_code, 200)

    def test_invalid_urls_for_logged_out_users(self):
        login_page = '/login/'
        urls = ['/stockpicker/IBOV', '/stockpicker/IFIX', '/stocktracker',
                '/forum/', '/graph', '/alerts/', '/carteira']
        for url in urls:
            #test 'must be logged in':
            response = self.client.post(url)
            self.assertEqual(response.status_code, 302)
            #test redirect to login page:
            response = self.client.post(url, follow=True)
            redirect_path = response.request.get('PATH_INFO')
            self.assertEqual(redirect_path, login_page)
            self.assertEqual(response.status_code, 200)

    def test_logged_out_user_access_admin_panel(self):
        response = self.client.post('/admin/')
        self.assertEqual(response.status_code, 302)