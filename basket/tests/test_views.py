import json

from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse
from products.models import Category, SubCategory, Product
from users.models import CustomUser
from basket.models import Basket


# class TestAddBasket(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(username='testuser', password='password1234')
#         self.client.login(username='testuser', password='password1234')
#
#         self.category = Category.objects.create(title='Category')
#         self.category.save()
#
#         self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
#         self.subcategory.save()
#
#         self.product = Product.objects.create(title='Title', price=1000, discount=10,
#                                               subcategory=self.subcategory)
#         self.product.save()
#
#         self.basket = Basket.objects.create(owner=self.user, product=self.product)
#         self.basket.save()
#
#     def tearDown(self):
#         self.product.delete()
#         self.subcategory.delete()
#         self.category.delete()
#         self.user.delete()
#
#     def test_correct(self):
#         response = self.client.get(reverse('basket:basket_add', kwargs={'product_slug': 'title'}))
#         data = response.content.decode('utf-8')
#         data = json.loads(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['status'], 'success')
#
#     def test_add_exists_product(self):
#         response = self.client.get(reverse('basket:basket_add', kwargs={'product_slug': 'title'}))
#         response = self.client.get(reverse('basket:basket_add', kwargs={'product_slug': 'title'}))
#         data = response.content.decode('utf-8')
#         data = json.loads(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['status'], 'success')
#
#     def test_create_with_not_exists_product(self):
#         response = self.client.get(reverse('basket:basket_add', kwargs={'product_slug': 'not_exists_slug'}))
#         data = response.content.decode('utf-8')
#         data = json.loads(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['status'], 'error')


# class TestChangeCountProductInBasket(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = CustomUser.objects.create_user(username='testuser', password='password1234')
#         self.client.login(username='testuser', password='password1234')
#
#         self.category = Category.objects.create(title='Category')
#         self.category.save()
#
#         self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
#         self.subcategory.save()
#
#         self.product = Product.objects.create(title='Title', price=1000, discount=10,
#                                               subcategory=self.subcategory)
#         self.product.save()
#
#         self.basket = Basket.objects.create(owner=self.user, count=10, product=self.product)
#         self.basket.save()
#
#     def tearDown(self):
#         self.product.delete()
#         self.subcategory.delete()
#         self.category.delete()
#         self.user.delete()
#
#     def test_correct(self):
#         response = self.client.get(reverse('basket:change_count', kwargs={'product_slug': 'title', 'operation': '-'}))
#         data = response.content.decode('utf-8')
#         data = json.loads(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['status'], 'success')
#         print(self.basket.count)
#
#     def test_with_incorrect_operation(self):
#         response = self.client.get(reverse('basket:change_count', kwargs={'product_slug': 'title', 'operation': 'text'}))
#         data = response.content.decode('utf-8')
#         data = json.loads(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['status'], 'success')
#         print(self.basket.count)
#
#     def test_with_not_exists_product(self):
#         response = self.client.get(reverse('basket:change_count', kwargs={'product_slug': 'not_exists_slug', 'operation': 'text'}))
#         data = response.content.decode('utf-8')
#         data = json.loads(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['status'], 'error')


class TestDeleteBasket(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='password1234')
        self.client.login(username='testuser', password='password1234')

        self.category = Category.objects.create(title='Category')
        self.category.save()

        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()

        self.product = Product.objects.create(title='Title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()

        self.basket = Basket.objects.create(owner=self.user, count=10, product=self.product)
        self.basket.save()

    def tearDown(self):
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()
        self.user.delete()

    def test_correct(self):
        response = self.client.get(reverse('basket:delete_basket', kwargs={'product_slug': 'title'}))
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_delete_all(self):
        response = self.client.get(reverse('basket:delete_basket', kwargs={'product_slug': '__all__'}))
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_with_not_exists_product(self):
        response = self.client.get(reverse('basket:delete_basket', kwargs={'product_slug': 'not_exists_slug'}))
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('basket:delete_basket', kwargs={'product_slug': 'title'}))
        self.assertEqual(response.status_code, 302)

