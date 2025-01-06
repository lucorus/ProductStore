import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.basket.models import Basket
from apps.users.models import CustomUser, Comment
from apps.products.models import Product, Category, SubCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')


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
def basket(user, product):
    return Basket.objects.create(owner=user, product=product, count=1)


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_get_profile(authenticated_client, basket):
    url = reverse('profile')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'user' in response.data
    assert 'basket' in response.data
    assert len(response.data['basket']) == 1


@pytest.mark.django_db
def test_get_profile_with_pagination(authenticated_client, basket):
    url = reverse('profile')
    response = authenticated_client.get(f"{url}?page=0", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['basket']) == 1

    response = authenticated_client.get(f"{url}?page=1", format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['basket']) == 0


@pytest.mark.django_db
def test_update_profile(authenticated_client):
    url = reverse('profile')
    data = {'username': 'newusername', 'email': 'newemail@example.com'}
    response = authenticated_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    authenticated_client.handler._force_user.refresh_from_db()
    assert authenticated_client.handler._force_user.username == 'newusername'
    assert authenticated_client.handler._force_user.email == 'newemail@example.com'


@pytest.mark.django_db
def test_update_profile_with_invalid_data(authenticated_client):
    url = reverse('profile')
    data = {'username': '', 'email': 'invalid-email'}
    response = authenticated_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
