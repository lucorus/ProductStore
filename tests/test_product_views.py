import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from apps.products.models import Product, Category, SubCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def category():
    return Category.objects.create(title='Test Category', slug='test-category')


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(title='Test SubCategory', category=category, slug='test-subcategory')


@pytest.fixture
def product(subcategory):
    return Product.objects.create(
        title='Test Product',
        price=100,
        subcategory=subcategory,
        slug='test-product'
    )


@pytest.fixture
def another_product(subcategory):
    return Product.objects.create(
        title='Another Test Product',
        price=200,
        subcategory=subcategory,
        slug='another-test-product'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_list_products(authenticated_client, product, another_product):
    url = reverse('product-list')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_list_products_with_pagination(authenticated_client, product, another_product):
    url = reverse('product-list')
    response = authenticated_client.get(f"{url}?page=0", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    response = authenticated_client.get(f"{url}?page=1", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_retrieve_product(authenticated_client, product):
    url = reverse('product-detail', kwargs={'pk': product.slug})
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['slug'] == product.slug


@pytest.mark.django_db
def test_retrieve_non_existent_product(authenticated_client):
    url = reverse('product-detail', kwargs={'pk': 'non-existent-product'})
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
