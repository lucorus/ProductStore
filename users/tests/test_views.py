from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
import json


class TestProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='password1234')
        self.client.login(username='testuser', password='password1234')

    def tearDown(self) -> None:
        self.user.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)


class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()

    def test_with_correct_data(self):
        response = self.client.post(reverse('users:register'), data={'username': 'username',
                                                                     'password': 'password_1234',
                                                                     'email': 'mail@gmail.com'})
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_with_incorrect_data(self):
        response = self.client.post(reverse('users:register'), data={'username': 'username',
                                                                     'password': 'none',
                                                                     'email': 'mail@gmail.com'})
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')


class UserLoginTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = CustomUser.objects.create(username='testuser', password='password1234')

    def tearDown(self) -> None:
        self.user.delete()

    def test_post_method_with_valid_data(self):
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'password1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))
        self.assertTrue(self.client.login)

    def test_post_method_with_invalid_data(self):
        self.client.logout()
        response = self.client.post(reverse('users:login'), {'username': 'not_used_username', 'password': 'password1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))

    def test_with_login_user(self):
        self.client.login(username='test_user2', password='12345')
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': '12345'})
        self.assertTrue(self.client.login)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))


class UserLogoutViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self) -> None:
        self.user.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
