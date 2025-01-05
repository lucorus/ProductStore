import pytest
from django.utils.text import slugify

from apps.users.models import CustomUser


@pytest.fixture
def setup_data():
    user = CustomUser.objects.create(username='testuser', password='password1234')
    return user


@pytest.mark.django_db
def test_custom_user_creation(setup_data):
    user = setup_data
    assert user.username == 'testuser'
    assert user.slug == slugify('testuser')
    assert user.can_write_comments is True


@pytest.mark.django_db
def test_custom_user_methods(setup_data):
    user = setup_data
    assert user.count_created_complaints() == 0
    assert user.count_received_complaints() == 0
    assert user.count_comments() == 0
