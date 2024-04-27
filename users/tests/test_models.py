from django.test import TestCase
from users.models import CustomUser


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(username='username', email='mail@gmail.com', password='password1234')
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_comparison_data(self):
        self.assertEqual(self.user.username, 'username')
        self.assertEqual(self.user.slug, 'username')
        self.assertEqual(self.user.email, 'mail@gmail.com')
