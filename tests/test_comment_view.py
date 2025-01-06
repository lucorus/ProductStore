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
def test_create_comment(authenticated_client, product):
    url = reverse('comments')
    data = {'product_slug': 'test-product', 'text': 'New Comment', 'estimation': 4}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.filter(author=authenticated_client.handler._force_user, product=product, text='New Comment').exists()


@pytest.mark.django_db
def test_create_comment_with_invalid_product(authenticated_client):
    url = reverse('comments')
    data = {'product_slug': 'invalid-product', 'text': 'New Comment', 'estimation': 4}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"message": "Продукт не найден"}


@pytest.mark.django_db
def test_create_reply_to_comment(authenticated_client, product, comment):
    url = reverse('comments')
    data = {'product_slug': 'test-product', 'text': 'Reply to Comment', 'comment_id': comment.id}
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert comment.answers.filter(author=authenticated_client.handler._force_user, text='Reply to Comment').exists()


@pytest.mark.django_db
def test_update_comment(authenticated_client, comment):
    url = reverse('comments')
    data = {'comment_id': comment.id, 'text': 'Updated Comment', 'estimation': 3}
    response = authenticated_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    comment.refresh_from_db()
    assert comment.text == 'Updated Comment'
    assert comment.estimation == 3


@pytest.mark.django_db
def test_update_comment_not_found(authenticated_client):
    url = reverse('comments')
    data = {'comment_id': 9999, 'text': 'Updated Comment', 'estimation': 3}
    response = authenticated_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"message": "Комментарий не найден"}


@pytest.mark.django_db
def test_get_comments_for_product(authenticated_client, product, comment):
    url = reverse('comments')
    data = {'product_slug': product.slug}
    response = authenticated_client.get(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'comments' in response.data
    assert len(response.data['comments']) == 1


@pytest.mark.django_db
def test_get_replies_for_comment(authenticated_client, product, comment):
    reply = Comment.objects.create(author=comment.author, product=product, text='Reply to Comment', estimation=0)
    comment.answers.add(reply)
    url = reverse('comments')
    data = {'comment_id': comment.id}
    response = authenticated_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'comments' in response.data
    assert len(response.data['comments']) == 1


@pytest.mark.django_db
def test_get_comments_for_invalid_product(authenticated_client):
    url = reverse('comments')
    data = {'product_slug': 'invalid-product'}
    response = authenticated_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"message": "Продукт не найден"}


@pytest.mark.django_db
def test_get_replies_for_invalid_comment(authenticated_client):
    url = reverse('comments')
    data = {'comment_id': 9999}
    response = authenticated_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"message": "Комментарий не найден"}


@pytest.mark.django_db
def test_delete_comment(authenticated_client, comment):
    url = reverse('comments')
    data = {'comment_id': comment.id}
    response = authenticated_client.delete(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_delete_comment_not_found(authenticated_client):
    url = reverse('comments')
    data = {'comment_id': 9999}
    response = authenticated_client.delete(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"message": "Комментарий не найден"}
