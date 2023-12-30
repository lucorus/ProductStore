from django.contrib.auth import authenticate
from django.test import TestCase
from . import models
import json


class CustomUserTest(TestCase):
    def setUp(self):
        self.user = models.CustomUser.objects.create_user(username='test', password='password1234',
                                                          email='test@gmail.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='password1234')
        self.assertTrue(user is not None)

    def test_wrong_username(self):
        user = authenticate(username='test123', password='password1234')
        self.assertTrue(user is None)

    def test_wrong_password(self):
        user = authenticate(username='test', password='password')
        self.assertTrue(user is None)


class RegistrationViewTest(TestCase):

    def test_get_correct(self):
        response = self.client.get('/user/registration')
        self.assertEqual(response.status_code, 200)

    def test_post_correct(self):
        response = self.client.post('/user/registration', {'username': 'user', 'password': 'password123',
                                                           'email': 'mail@gmail.com'})
        data = response.content.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_post_incorrect(self):
        response = self.client.post('/user/registration', {'username': 'user', 'password': 'pass',
                                                           'email': 'mail@gmail.com'})
        data = response.content.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['errors']['password'], 'Пароль должен состоять минимум из 8 символов')
