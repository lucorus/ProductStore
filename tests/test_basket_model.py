import pytest
from django.db import IntegrityError

from apps.basket.models import Basket
from apps.users.models import CustomUser
from apps.products.models import Product, Category, SubCategory


@pytest.fixture
def setup_data():
    category = Category.objects.create(title='Category')
    subcategory = SubCategory.objects.create(title='Subcategory', category=category)
    product = Product.objects.create(title='Title', price=1000, discount=10, subcategory=subcategory)
    user = CustomUser.objects.create(username='username', email='mail@gmail.com', password='password1234')
    basket = Basket.objects.create(owner=user, product=product, count=1)
    return basket, user, product


@pytest.mark.django_db
def test_comparison_data(setup_data):
    basket, user, product = setup_data
    assert basket.owner == user
    assert basket.product == product
    assert basket.count == 1
    assert basket.get_count_products_in_basket() == 1
    assert basket.get_sum_products() == 900


@pytest.mark.django_db
def test_negative_count(setup_data):
    basket, _, _ = setup_data
    with pytest.raises(IntegrityError):
        basket.count = -1
        basket.save()
