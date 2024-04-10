from django.test import TestCase
from django.urls import reverse
from products import models, views


class DetailViewTest(TestCase):

    def setUp(self):
        self.photo = models.ProductPhoto.objects.create(product_photo='photo.png')
        self.photo.save()
        self.category = models.Category.objects.create(title='category', slug='category',
                                                       image='category_image.png')
        self.category.save()
        self.subcategory = models.SubCategory.objects.create(title='subcategory', slug='subcategory',
                                                             image='subcategory_image.png',
                                                             category=self.category)
        self.subcategory.save()
        self.product = models.Product.objects.create(title='product', slug='product',
                                                     price=200, subcategory=self.subcategory)
        self.product.photos.add(self.photo)
        self.product.save()

    def test_correct(self):
        response = self.client.get(f'/detail/{self.product.slug}')
        self.assertEqual(response.status_code, 200)

    def test_not_found_slug(self):
        response = self.client.get('/detail/not_found_slug')
        self.assertEqual(response.status_code, 404)


class ProductInCategoryViewTest(TestCase):
    def setUp(self):
        self.photo = models.ProductPhoto.objects.create(product_photo='photo.png')
        self.photo.save()
        self.category = models.Category.objects.create(title='category', slug='category',
                                                       image='category_image.png')
        self.category.save()
        self.subcategory = models.SubCategory.objects.create(title='subcategory', slug='subcategory',
                                                             image='subcategory_image.png',
                                                             category=self.category)
        self.subcategory.save()
        self.product = models.Product.objects.create(title='product', slug='product',
                                                     price=200, subcategory=self.subcategory)
        self.product.photos.add(self.photo)
        self.product.save()

    def test_correct(self):
        response = self.client.get(f'/category/{ self.category.slug }')
        self.assertEqual(response.status_code, 200)

    def test_not_found_slug(self):
        response = self.client.get('/category/not_found_category_slug')
        self.assertEqual(response.status_code, 404)

