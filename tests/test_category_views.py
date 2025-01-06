import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.products.models import  Category, SubCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category():
    return Category.objects.create(title='Test Category', slug='test-category')


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(title='Test SubCategory', category=category, slug='test-subcategory')


@pytest.fixture
def another_category():
    return Category.objects.create(title='Another Category', slug='another-category')


@pytest.fixture
def another_subcategory(another_category):
    return SubCategory.objects.create(title='Another SubCategory', category=another_category, slug='another-subcategory')


@pytest.mark.django_db
def test_get_all_subcategories(api_client, subcategory, another_subcategory):
    url = reverse('categories')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_subcategories_by_category_slugs(api_client, category, subcategory, another_category,
                                             another_subcategory):
    url = reverse('categories')
    data = {'groups_slugs': 'test-category'}
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['slug'] == 'test-subcategory'


@pytest.mark.django_db
def test_get_subcategories_with_pagination(api_client, subcategory, another_subcategory):
    url = reverse('categories')
    data = {'page': 0}
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    data = {'page': 1}
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_get_subcategories_with_invalid_category_slugs(api_client):
    url = reverse('categories')
    data = {'groups_slugs': ['invalid-category']}
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
