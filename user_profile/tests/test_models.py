from django.contrib.auth import authenticate
from django.test import TestCase
from user_profile import models
from products import models as product_models
import json


class CustomUserTest(TestCase):
    def setUp(self):
        self.user = models.CustomUser.objects.create_user(username='test', password='password1234',
                                                          email='test@gmail.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='password1234')
        self.assertTrue(user is not None)

    def test_wrong_username(self):
        user = authenticate(username='test123', password='password1234')
        self.assertTrue(user is None)

    def test_wrong_password(self):
        user = authenticate(username='test', password='password')
        self.assertTrue(user is None)


class CommentTest(TestCase):
    def setUp(self):
        self.user = models.CustomUser.objects.create_user(username='test', password='password1234',
                                                          email='test@gmail.com')
        self.user.save()
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
        self.comment = models.Comments.objects.create(text='comment_text',
                                                      author=self.user,
                                                      product=self.product,
                                                      estimation=4)
        self.comment.save()

    def tearDown(self):
        self.product.delete()
        self.photo.delete()
        self.category.delete()
        self.user.delete()
        self.comment.delete()

    def test_correct(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.product, self.product)

    def test_create_incorrect(self):
        new_comment = models.Comments.objects.create(text='comment_text',
                                                     author=self.user,
                                                     product=self.product,
                                                     estimation=6)
        new_comment.save()
        self.assertTrue(new_comment is not None)
        self.assertEqual(new_comment.estimation, 5)
        new_comment.delete()
