from django.template import RequestContext
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from user_profile import models, views
from products import models as product_models
import json


class RegistrationTest(TestCase):

    def test_get_correct(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_post_correct(self):
        response = self.client.post(reverse('register'), {'username': 'user', 'password': 'password123',
                                                          'email': 'mail@gmail.com'})
        data = response.content.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(models.CustomUser.objects.get(id=1))

    def test_post_incorrect(self):
        response = self.client.post(reverse('register'), {'username': 'user', 'password': 'pass',
                                                          'email': 'mail@gmail.com'})
        data = response.content.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'error')
        user = None
        try:
            user = models.CustomUser.objects.get(id=1)
        except:
            self.assertIsNone(user)


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.response = self.client.get('/')
        self.request = self.factory.get("/")
        self.request.session = self.client.session

        self.context = RequestContext(self.request)
        self.client = Client()
        self.user = models.CustomUser.objects.create(username='testuser', slug='testuser',
                                                     password='password1234')

    def TeatDown(self):
        self.user.delete()

    def test_get_method(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_post_method_with_valid_data(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('main_page'))
        self.assertTrue(self.client.login)

    def test_post_method_with_invalid_data(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {'username': 'not_used_username', 'password': 'password1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('main_page'))

    def test_with_login_user(self):
        self.client.login(username='test_user2', password='12345')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertTrue(self.client.login)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('main_page'))


class ProfileTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = models.CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.photo = product_models.ProductPhoto.objects.create(product_photo='photo.png')
        self.photo.save()
        self.category = product_models.Category.objects.create(title='category_title', slug='category_title',
                                                               image='category_image.png')
        self.category.save()
        self.subcategory = product_models.SubCategory.objects.create(title='subcategory_title',
                                                                     slug='subcategory_title',
                                                                     image='subcategory_image.png',
                                                                     category=self.category)
        self.subcategory.save()
        self.product = product_models.Product.objects.create(title='product', slug='product',
                                                             price=200, subcategory=self.subcategory)
        self.product.photos.add(self.photo)
        self.product.save()

        self.session = self.client.session
        self.session['products'] = ['product']
        self.session.save()

    def tearDown(self):
        self.user.delete()
        self.client.session.clear()
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/profile.html')
        self.assertEqual(response.context[0]['object_list']['product_objects']['product'], self.product)

    def test_get_empty_basket(self):
        # очищаем корзину пользователя
        self.session['products'] = []
        self.session.save()

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/profile.html')
        self.assertIsNone(response.context[0]['object_list']['product_objects'].get('product'))

    def test_with_logout_user(self):
        response = Client().get(reverse('profile'))
        self.assertEqual(response.status_code, 302)


class AddProductToSessionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = models.CustomUser.objects.create_user(username='testuser', password='password1234')
        self.client.login(username='testuser', password='password1234')

        self.category = product_models.Category.objects.create(title='category_title', slug='category_title',
                                                               image='category_image.png')
        self.category.save()
        self.subcategory = product_models.SubCategory.objects.create(title='subcategory_title',
                                                                     slug='subcategory_title',
                                                                     image='subcategory_image.png',
                                                                     category=self.category)
        self.subcategory.save()
        self.product = product_models.Product.objects.create(title='product', slug='product',
                                                             price=200, subcategory=self.subcategory)
        self.product.save()

    def tearDown(self):
        self.user.delete()
        self.client.session.clear()
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('add_to_basket'), {'product_slug': 'product'})
        data = response.content.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(self.client.session['products'], {'product': {'price': 200, 'count': 1}})

    def test_add_to_basket_not_exist_product(self):
        response = self.client.get(reverse('add_to_basket'), {'product_slug': 'not_exist_product'})
        data = response.content.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertIsNone(self.client.session.get('products'))

    def test_with_logout_user(self):
        response = Client().get(reverse('add_to_basket'))
        self.assertEqual(response.status_code, 302)


class ClearBasketTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = models.CustomUser.objects.create_user(username='testuser', password='password1234')
        self.client.login(username='testuser', password='password1234')

        self.category = product_models.Category.objects.create(title='category_title', slug='category_title',
                                                               image='category_image.png')
        self.category.save()
        self.subcategory = product_models.SubCategory.objects.create(title='subcategory_title',
                                                                     slug='subcategory_title',
                                                                     image='subcategory_image.png',
                                                                     category=self.category)
        self.subcategory.save()
        self.product = product_models.Product.objects.create(title='product', slug='product',
                                                             price=200, subcategory=self.subcategory)
        self.product.save()
        self.client.session['products'] = {self.product.slug: {'price': self.product.price, 'count': 1}}

    def tearDown(self):
        self.user.delete()
        self.client.session.clear()
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('clear_basket'))
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(self.client.session['products'], {})

    def test_with_empty_basket(self):
        response = self.client.get(reverse('clear_basket'))
        data = response.content.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(self.client.session['products'], {})

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('clear_basket'))
        self.assertEqual(response.status_code, 302)


class AddProductToFavoriteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = models.CustomUser.objects.create_user(username='testuser', password='password1234')
        self.client.login(username='testuser', password='password1234')

        self.category = product_models.Category.objects.create(title='category_title', slug='category_title',
                                                               image='category_image.png')
        self.category.save()
        self.subcategory = product_models.SubCategory.objects.create(title='subcategory_title',
                                                                     slug='subcategory_title',
                                                                     image='subcategory_image.png',
                                                                     category=self.category)
        self.subcategory.save()
        self.product = product_models.Product.objects.create(title='product', slug='product',
                                                             price=200, subcategory=self.subcategory)
        self.product.save()

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.get(reverse('add_to_favorites'), data={'product_id': self.product.id})
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product.users.first().username, self.user.username)

    def test_delete_product_into_favorites(self):
        # добавили в избранное
        response = self.client.get(reverse('add_to_favorites'), data={'product_id': self.product.id})
        # удалили из избранного
        response = self.client.get(reverse('add_to_favorites'), data={'product_id': self.product.id})
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.product.users.first())

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.get(reverse('add_to_favorites'), data={'product_id': self.product.id})
        self.assertEqual(response.status_code, 302)

    def test_with_not_exist_product(self):
        self.client.login(username='testuser', password='password1234')
        response = self.client.get(reverse('add_to_favorites'), data={'product_id': self.product.id + 1})
        data = response.content.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 200)


class CreateCommentTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = models.CustomUser.objects.create_user(username='testuser', password='password1234')
        self.client.login(username='testuser', password='password1234')

        self.category = product_models.Category.objects.create(title='category_title', slug='category_title',
                                                               image='category_image.png')
        self.category.save()
        self.subcategory = product_models.SubCategory.objects.create(title='subcategory_title',
                                                                     slug='subcategory_title',
                                                                     image='subcategory_image.png',
                                                                     category=self.category)
        self.subcategory.save()
        self.product = product_models.Product.objects.create(title='product', slug='product',
                                                             price=200, subcategory=self.subcategory)
        self.product.save()

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.subcategory.delete()
        self.category.delete()

    def test_correct(self):
        response = self.client.post(reverse('create_comment'),
                                    data={'product_slug': self.product.slug,
                                          'text': 'text', 'estimation': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Comments.objects.first().product.slug, self.product.slug)

    def test_with_logout_user(self):
        self.client.logout()
        response = self.client.post(reverse('create_comment'),
                                    data={'product_slug': self.product.slug,
                                          'text': 'text', 'estimation': 3})
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(models.Comments.objects.first())
