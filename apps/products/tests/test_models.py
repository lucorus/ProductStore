from unittest import TestCase
from django.db import IntegrityError
from products.models import Product, SubCategory, Category


class TestProduct(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()

    def tearDown(self):
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_comparison_data(self):
        self.assertEqual(self.product.slug, 'title')
        self.assertEqual(self.product.subcategory, self.subcategory)
        self.assertEqual(self.product.subcategory.category, self.category)
        self.assertEqual(self.product.price_with_discount(), 900)

    def test_negative_price(self):
        try:
            self.product.price = -100
            self.product.save()
        except Exception as ex:
            self.assertEqual(type(ex), IntegrityError)

    def test_long_discount(self):
        try:
            self.product.discount = 10.111
            self.product.save()
        except Exception as ex:
            self.assertEqual(type(ex), IntegrityError)

    def test_get_unshowing_objects(self):
        self.product.showing = False
        self.product.save()
        product = Product.objects.showing_products().filter(slug='title')
        self.assertEqual(list(product), [])


class TestCategory(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()

    def tearDown(self):
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_comparison_data(self):
        self.assertEqual(self.category.slug, 'category')
        self.assertEqual(self.category.subcategories.first(), self.subcategory)
        self.assertEqual(self.category.subcategories.first().product.first(), self.product)


class TestSubCategory(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()

    def tearDown(self):
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_comparison_data(self):
        self.assertEqual(self.subcategory.slug, 'subcategory')
        self.assertEqual(self.subcategory.category, self.category)
        self.assertEqual(self.subcategory.product.first(), self.product)
