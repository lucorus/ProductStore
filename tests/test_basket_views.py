import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser
from apps.products.models import Product, Category, SubCategory
from apps.basket.models import Basket


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def category():
    return Category.objects.create(title='Test Category')


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(title='Test SubCategory', category=category)


@pytest.fixture
def product(subcategory):
    return Product.objects.create(
        title='Test Product',
        price=100,
        subcategory=subcategory,
        slug='test-product'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_add_product_to_basket(authenticated_client, product):
    url = reverse('basket')
    data = {'product_slug': 'test-product'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Basket.objects.filter(owner=authenticated_client.handler._force_user, product=product).exists()


@pytest.mark.django_db
def test_remove_product_from_basket(authenticated_client, product):
    Basket.objects.create(owner=authenticated_client.handler._force_user, product=product)
    url = reverse('basket')
    data = {'product_slug': 'test-product'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Basket.objects.filter(owner=authenticated_client.handler._force_user, product=product).exists()


@pytest.mark.django_db
def test_clear_basket(authenticated_client, product):
    Basket.objects.create(owner=authenticated_client.handler._force_user, product=product)
    url = reverse('basket')
    data = {'product_slug': '__all'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert not Basket.objects.filter(owner=authenticated_client.handler._force_user).exists()


@pytest.mark.django_db
def test_change_product_count_in_basket(authenticated_client, product):
    basket_item = Basket.objects.create(owner=authenticated_client.handler._force_user, product=product, count=1)
    url = reverse('basket')
    data = {'product_slug': 'test-product', 'different_count': 2}
    response = authenticated_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    basket_item.refresh_from_db()
    assert basket_item.count == 3


@pytest.mark.django_db
def test_remove_product_from_basket_when_count_is_zero(authenticated_client, product):
    basket_item = Basket.objects.create(owner=authenticated_client.handler._force_user, product=product, count=1)
    url = reverse('basket')
    data = {'product_slug': 'test-product', 'different_count': -1}
    response = authenticated_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert not Basket.objects.filter(owner=authenticated_client.handler._force_user, product=product).exists()


@pytest.mark.django_db
def test_product_not_found(authenticated_client):
    url = reverse('basket')
    data = {'product_slug': 'non-existent-product'}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "Продукт не найден"


@pytest.mark.django_db
def test_no_data_provided(authenticated_client):
    url = reverse('basket')
    data = {}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "Данные не переданы"
