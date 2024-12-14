from django.test import TestCase
from django.db import IntegrityError
from products.models import Category, SubCategory, Product
from users.models import CustomUser
from basket.models import Basket


class TestBasket(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()

        self.user = CustomUser.objects.create(username='username', email='mail@gmail.com', password='password1234')
        self.user.save()

        self.basket = Basket.objects.create(owner=self.user, product=self.product, count=1)
        self.basket.save()

    def tearDown(self) -> None:
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()
        self.user.delete()

    def test_comparison_data(self):
        self.assertEqual(self.basket.owner, self.user)
        self.assertEqual(self.basket.product, self.product)
        self.assertEqual(self.basket.count, 1)
        self.assertEqual(self.basket.get_count_products_in_basket(), 1)
        self.assertEqual(self.basket.get_sum_products(), 900)

    def test_negative_count(self):
        try:
            self.basket.count = -1
        except Exception as ex:
            self.assertEqual(type(ex), IntegrityError)
