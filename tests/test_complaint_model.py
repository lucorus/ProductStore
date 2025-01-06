import pytest

from apps.users.models import CustomUser, Comment, Complaints
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
def test_complaints_creation(setup_data):
    user, _, comment = setup_data
    complaint = Complaints.objects.create(author=user, comment=comment)
    assert complaint.author == user
    assert complaint.comment == comment
    assert complaint.is_reviewed is False


@pytest.mark.django_db
def test_complaints_save_method(setup_data):
    user, _, comment = setup_data
    complaint1 = Complaints.objects.create(author=user, comment=comment)
    complaint2 = Complaints.objects.create(author=user, comment=comment)
    complaint1.is_reviewed = True
    complaint1.save()
    assert Complaints.objects.filter(comment=comment, is_reviewed=True).count() == 2


@pytest.mark.django_db
def test_complaints_save_method_without_changing_others(setup_data):
    user, _, comment = setup_data
    complaint1 = Complaints.objects.create(author=user, comment=comment)
    complaint2 = Complaints.objects.create(author=user, comment=comment)
    complaint1.is_reviewed = True
    complaint1.save(change_other_complaints=False)
    assert Complaints.objects.filter(comment=comment, is_reviewed=True).count() == 1