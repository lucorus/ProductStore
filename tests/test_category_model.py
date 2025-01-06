import pytest
from django.db import IntegrityError
from slugify import slugify

from apps.products.models import Product, SubCategory, Category


@pytest.fixture
def setup_data():
    category = Category.objects.create(title='Test Category')
    return category


@pytest.mark.django_db
def test_category_creation(setup_data):
    category = setup_data
    assert category.title == 'Test Category'
    assert category.slug == slugify('Test Category')


@pytest.mark.django_db
def test_unique_title():
    Category.objects.create(title='Unique Category')
    with pytest.raises(IntegrityError):
        Category.objects.create(title='Unique Category')
