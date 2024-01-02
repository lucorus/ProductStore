from django.test import TestCase
from . import models


class ProductTest(TestCase):
    def setUp(self):
        self.photo = models.ProductPhoto.objects.create(product_photo='photo.png')
        self.photo.save()
        self.category = models.Category.objects.create(title='category_title', slug='category_title',
                                                      image='category_image.png')
        self.category.save()
        self.subcategory = models.SubCategory.objects.create(title='subcategory_title', slug='subcategory_title',
                                                             image='subcategory_image.png',
                                                             category=self.category)
        self.subcategory.save()
        self.product = models.Product.objects.create(title='product', slug='product',
                                                     price=200, subcategory=self.subcategory)
        self.product.photos.add(self.photo)
        self.product.save()

    def tearDown(self):
        self.product.delete()
        self.photo.delete()
        self.category.delete()

    def test_correct(self):
        self.assertEqual(self.product.title, 'product')
        self.assertEqual(self.product.slug, 'product')
        self.assertEqual(self.product.price, 200)
        self.assertEqual(self.product.subcategory.category.title, 'category_title')
        self.assertEqual(self.product.subcategory.title, 'subcategory_title')

    def test_update_product_title(self):
        self.product.title, self.product.slug = 'new_product_title', 'new_product_slug'
        self.product.save()
        self.assertEqual(self.product.title, 'new_product_title')
        self.assertEqual(self.product.slug, 'new_product_slug')


class ProductPhotoTest(TestCase):
    def setUp(self):
        self.product_photos = models.ProductPhoto.objects.create(product_photo='product_photo.png')
        self.product_photos.save()

    def tearDown(self):
        self.product_photos.delete()

    def test_photo(self):
        self.assertEqual(self.product_photos.product_photo, 'product_photo.png')

    def test_change_photo(self):
        self.product_photos.product_photo = 'new_product_photo.png'
        self.product_photos.save()
        self.assertEqual(self.product_photos.product_photo, 'new_product_photo.png')


class CategoryTest(TestCase):
    def setUp(self):
        self.category = models.Category.objects.create(title='category_title', slug='category_title',
                                                       image='category_image.png')
        self.category.save()

    def tearDown(self):
        self.category.delete()

    def test_get_fields(self):
        self.assertEqual(self.category.title, 'category_title')
        self.assertEqual(self.category.slug, 'category_title')
        self.assertEqual(self.category.image, 'category_image.png')

    def test_change_fields(self):
        self.category.title, self.category.slug = 'new_category_title', 'new_category_slug'
        self.assertEqual(self.category.title, 'new_category_title')
        self.assertEqual(self.category.slug, 'new_category_slug')


class SubCategoryTest(TestCase):
    def setUp(self):
        self.category = models.Category.objects.create(title='category_title', slug='category_title',
                                                       image='category_image.png')
        self.category.save()
        self.subcategory = models.SubCategory.objects.create(title='subcategory_title', slug='subcategory_slug',
                                                             image='subcategory_image.png', category=self.category)
        self.subcategory.save()

    def tearDown(self):
        self.subcategory.delete()

    def test_get_fields(self):
        self.assertEqual(self.subcategory.title, 'subcategory_title')
        self.assertEqual(self.subcategory.category.title, 'category_title')
        self.assertEqual(self.subcategory.image, 'subcategory_image.png')


class CommentTest(TestCase):
    def setUp(self):
        self.user = models.CustomUser.objects.create_user(username='test', password='password1234',
                                                          email='test@gmail.com')
        self.user.save()
        self.photo = models.ProductPhoto.objects.create(product_photo='photo.png')
        self.photo.save()
        self.category = models.Category.objects.create(title='category_title', slug='category_title',
                                                       image='category_image.png')
        self.category.save()
        self.subcategory = models.SubCategory.objects.create(title='subcategory_title', slug='subcategory_title',
                                                             image='subcategory_image.png',
                                                             category=self.category)
        self.subcategory.save()
        self.product = models.Product.objects.create(title='product', slug='product',
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
        self.new_comment = models.Comments.objects.create(text='comment_text',
                                                      author=self.user,
                                                      product=self.product,
                                                      estimation=6)
        self.new_comment.save()
        self.assertTrue(self.new_comment is not None)
        self.new_comment.delete()
