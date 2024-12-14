from products.models import Product, SubCategory, Category
from django.test import TestCase, Client
from django.urls import reverse
from types import NoneType
import json


class TestProducts(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_all_products(self):
        response = self.client.get(reverse('products:products'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(data['count']), int)
        self.assertIsNone(data['previous'])
        self.assertTrue(type(data['next']) in [NoneType, str])
        self.assertEqual(type(data['results']), list)

    def test_get_products_in_category(self):
        response = self.client.get(reverse('products:products'), data={'category': 'myaso'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(data['count']), int)
        self.assertIsNone(data['previous'])
        self.assertTrue(type(data['next']) in [NoneType, str])
        self.assertEqual(type(data['results']), list)

    def test_get_incorrect_category_and_subcategory(self):
        response = self.client.get(reverse('products:products'), data={'category': 'myaso', 'subcategory': 'syr'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 0)
        self.assertIsNone(data['previous'])
        self.assertTrue(type(data['next']) in [NoneType, str])
        self.assertEqual(type(data['results']), list)


class TestCategories(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_data(self):
        response = self.client.get(reverse('products:get_categories'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(data['count']), int)
        self.assertIsNone(data['previous'])
        self.assertTrue(type(data['next']) in [NoneType, str])
        self.assertEqual(type(data['results']), list)


class DetailProductTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()

    def test_get_data(self):
        response = self.client.get(reverse('products:product_detail', kwargs={'slug': 'title'}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['product']['title'], self.product.title)
        self.assertEqual(data['product']['subcategory']['title'], self.product.subcategory.title)

    def test_get_not_exists_product(self):
        response = self.client.get(reverse('products:product_detail', kwargs={'slug': 'not_exists_slug'}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')
