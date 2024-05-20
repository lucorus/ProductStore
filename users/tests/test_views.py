from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser, Comment, Complaints
from products.models import Product, Category, SubCategory
import json


class TestProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='password1234')
        self.client.login(username='testuser', password='password1234')

    def tearDown(self) -> None:
        self.user.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)


class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()

    def test_with_correct_data(self):
        response = self.client.post(reverse('users:register'), data={'username': 'username',
                                                                     'password': 'password_1234',
                                                                     'email': 'mail@gmail.com'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_with_incorrect_data(self):
        response = self.client.post(reverse('users:register'), data={'username': 'username',
                                                                     'password': 'none',
                                                                     'email': 'mail@gmail.com'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')


class UserLoginTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = CustomUser.objects.create(username='testuser', password='password1234')

    def tearDown(self) -> None:
        self.user.delete()

    def test_post_method_with_valid_data(self):
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'password1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))
        self.assertTrue(self.client.login)

    def test_post_method_with_invalid_data(self):
        self.client.logout()
        response = self.client.post(reverse('users:login'), {'username': 'not_used_username', 'password': 'password1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))

    def test_with_login_user(self):
        self.client.login(username='test_user2', password='12345')
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': '12345'})
        self.assertTrue(self.client.login)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))


class UserLogoutViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self) -> None:
        self.user.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('products:main_page'))

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)


class TestAddToFavorites(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', slug='title', price=1000, discount=10, subcategory=self.subcategory)
        self.product.save()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:add_to_favorites'), data={'product_slug': 'title'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(self.user.favorites.first().slug, 'title')

    def test_double_add_in_favorites(self):
        response = self.client.get(reverse('users:add_to_favorites'), data={'product_slug': 'title'})
        response = self.client.get(reverse('users:add_to_favorites'), data={'product_slug': 'title'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertIsNone(self.user.favorites.first())

    def test_without_data(self):
        response = self.client.get(reverse('users:add_to_favorites'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')
        self.assertIsNone(self.user.favorites.first())

    def test_with_not_found_product(self):
        response = self.client.get(reverse('users:add_to_favorites'), data={'product_slug': 'not_found_slug'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')
        self.assertIsNone(self.user.favorites.first())


class TestCreateComment(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', slug='title', price=1000, discount=10, subcategory=self.subcategory)
        self.product.save()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.post(
            reverse('users:create_comment', kwargs={'product_slug': self.product.slug}),
            data={'text': 'text', 'estimation': '5'}
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_logout_user(self):
        client = Client()
        response = client.post(
            reverse('users:create_comment', kwargs={'product_slug': self.product.slug}),
            data={'text': 'text', 'estimation': '5'}
        )
        self.assertEqual(response.status_code, 302)

    def test_with_not_exists_product(self):
        response = self.client.post(
            reverse('users:create_comment', kwargs={'product_slug': 'not_exists_slug'}),
            data={'text': 'text', 'estimation': '5'}
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')


class TestGetComments(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', slug='title', price=1000, discount=10, subcategory=self.subcategory)
        self.product.save()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.comment = Comment(author=self.user, product=self.product, text='text', estimation=5)
        self.comment.save()

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:get_comments', kwargs={'product_slug': self.product.slug}))
        data = json.loads(response.content)
        print(f'DATA  === {data}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['id'], self.comment.pk)

    def test_with_not_exists_product(self):
        response = self.client.get(reverse('users:get_comments', kwargs={'product_slug': 'not_exists_product_slug'}))
        data = json.loads(response.content)
        print(data, ' === DATA 2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'], [])


class TestGetAnswers(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', slug='title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.answer = Comment.objects.create(author=self.user, product=self.product, text='answer', estimation=0)
        self.answer.save()
        self.comment = Comment(author=self.user, product=self.product, text='text', estimation=5)
        self.comment.save()
        self.comment.answers.add(self.answer)
        self.comment.save()

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:get_answers', kwargs={'comment_id': self.comment.pk}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['id'], self.answer.id)

    def test_with_not_exists_comment(self):
        response = self.client.get(reverse('users:get_answers', kwargs={'comment_id': self.comment.pk+100}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'], [])


class CreateComplain(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', slug='title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.comment = Comment(author=self.user, product=self.product, text='text', estimation=5)
        self.comment.save()
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('users:create_complaint'), data={'comment_id': self.comment.pk})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_with_logout_user(self):
        response = Client().get(reverse('users:create_complaint'), data={'comment_id': self.comment.pk})
        self.assertEqual(response.status_code, 302)

    def test_with_not_exists_comment(self):
        response = self.client.get(reverse('users:create_complaint'), data={'comment_id': self.comment.pk+100})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')

    def test_without_data(self):
        response = self.client.get(reverse('users:create_complaint'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')

