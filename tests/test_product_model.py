import pytest
from django.db import IntegrityError
from django.utils.text import slugify

from apps.products.models import Product, SubCategory, Category


@pytest.fixture
def setup_data():
    category = Category.objects.create(title='Category')
    subcategory = SubCategory.objects.create(title='Subcategory', category=category)
    product = Product.objects.create(
        title='Test Product',
        price=1000,
        discount=10,
        subcategory=subcategory,
        showing=True
    )
    return product, subcategory


@pytest.mark.django_db
def test_product_creation(setup_data):
    product, _ = setup_data
    assert product.title == 'Test Product'
    assert product.price == 1000
    assert product.discount == 10
    assert product.showing is True
    assert product.slug == slugify('Test Product')


@pytest.mark.django_db
def test_price_with_discount(setup_data):
    product, _ = setup_data
    assert product.price_with_discount() == 900


@pytest.mark.django_db
def test_negative_price(setup_data):
    product, _ = setup_data
    with pytest.raises(IntegrityError):
        product.price = -100
        product.save()


@pytest.mark.django_db
def test_get_unshowing_objects(setup_data):
    product, _ = setup_data
    product.showing = False
    product.save()
    products = Product.objects.showing_products().filter(slug='test-product')
    assert list(products) == []
