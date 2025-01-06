import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser, Comment, Complaints
from apps.products.models import Product, Category, SubCategory


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
def comment(user, product):
    return Comment.objects.create(author=user, product=product, text='Test Comment', estimation=5)


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_create_complaint(authenticated_client, comment):
    url = reverse('complaints')
    data = {'comment_id': comment.id}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Complaints.objects.filter(author=authenticated_client.handler._force_user, comment=comment).exists()


@pytest.mark.django_db
def test_create_complaint_with_invalid_comment(authenticated_client):
    url = reverse('complaints')
    data = {'comment_id': 9999}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"message": "Комментарий не найден"}


@pytest.mark.django_db
def test_create_complaint_without_comment_id(authenticated_client):
    url = reverse('complaints')
    data = {}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"message": "Комментарий не найден"}
