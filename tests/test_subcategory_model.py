import pytest
from django.utils.text import slugify
from django.db import IntegrityError
from apps.products.models import SubCategory, Category


@pytest.fixture
def setup_data():
    category = Category.objects.create(title='Test Category')
    subcategory = SubCategory.objects.create(title='Test SubCategory', category=category)
    return subcategory, category


@pytest.mark.django_db
def test_subcategory_creation(setup_data):
    subcategory, category = setup_data
    assert subcategory.title == 'Test SubCategory'
    assert subcategory.category == category
    assert subcategory.slug == slugify('Test SubCategory')


@pytest.mark.django_db
def test_unique_title():
    category = Category.objects.create(title='Test Category')
    SubCategory.objects.create(title='Unique SubCategory', category=category)
    with pytest.raises(IntegrityError):
        SubCategory.objects.create(title='Unique SubCategory', category=category)
