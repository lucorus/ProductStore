import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser, Comment
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
def test_add_to_favorites(authenticated_client, product):
    url = reverse('favorite')
    data = {'product_slug': 'test-product'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert product in authenticated_client.handler._force_user.favorites.all()


@pytest.mark.django_db
def test_remove_from_favorites(authenticated_client, product):
    authenticated_client.handler._force_user.favorites.add(product)
    url = reverse('favorite')
    data = {'product_slug': 'test-product'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert product not in authenticated_client.handler._force_user.favorites.all()


@pytest.mark.django_db
def test_get_favorites(authenticated_client, product):
    authenticated_client.handler._force_user.favorites.add(product)
    url = reverse('favorite')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['slug'] == 'test-product'


@pytest.mark.django_db
def test_get_favorites_with_pagination(authenticated_client, product, another_product):
    authenticated_client.handler._force_user.favorites.add(product, another_product)
    url = reverse('favorite')
    response = authenticated_client.get(f"{url}?page=0", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    response = authenticated_client.get(f"{url}?page=1", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_add_to_favorites_without_slug(authenticated_client):
    url = reverse('favorite')
    data = {}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'status': 'error', 'message': 'product not found'}


@pytest.mark.django_db
def test_add_to_favorites_with_invalid_slug(authenticated_client):
    url = reverse('favorite')
    data = {'product_slug': 'invalid-product'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'status': 'error', 'message': 'product not found'}