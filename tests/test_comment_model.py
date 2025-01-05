import pytest

from apps.users.models import CustomUser, Comment
from apps.products.models import Product, Category, SubCategory


@pytest.fixture
def setup_data():
    category = Category.objects.create(title='Test Category')
    subcategory = SubCategory.objects.create(title='Test SubCategory', category=category)
    product = Product.objects.create(
        title='Test Product',
        price=1000,
        discount=10,
        subcategory=subcategory,
        showing=True
    )
    user = CustomUser.objects.create(username='testuser', password='password1234')
    comment = Comment.objects.create(
        author=user,
        product=product,
        text='Test comment',
        estimation=5
    )
    return user, product, comment


@pytest.mark.django_db
def test_comment_methods(setup_data):
    _, _, comment = setup_data
    assert comment.count_answers() == 0
    assert comment.get_answers() == []
