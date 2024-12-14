from django.test import TestCase
from products.models import Product, SubCategory, Category
from users.models import CustomUser, Comment, Complaints


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


class TestComment(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category')
        self.category.save()
        self.subcategory = SubCategory.objects.create(title='Subcategory', category=self.category)
        self.subcategory.save()
        self.product = Product.objects.create(title='Title', slug='title', price=1000, discount=10,
                                              subcategory=self.subcategory)
        self.product.save()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.answer = Comment.objects.create(author=self.user, product=self.product, text='answer', estimation=0)
        self.answer.save()
        self.comment = Comment(author=self.user, product=self.product, text='text', estimation=5)
        self.comment.save()
        self.comment.answers.add(self.answer)
        self.comment.save()

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def test_comparison_data(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.answers.first().author, self.user)
        self.assertTrue(self.comment.showing)
        self.assertEqual(self.comment.count_answers(), 1)
        self.assertEqual(
            self.comment.get_answers(),
            [{
                'pk': self.answer.pk,
                'text': self.answer.text,
                'author__username': self.answer.author.username,
                'author__slug': self.answer.author.slug
            }]
        )

    def save_with_big_estimation(self):
        self.comment.estimation = 99999999
        self.comment.save()
        self.assertEqual(self.comment.estimation, 5)


class TestComplaints(TestCase):
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
        self.complaint = Complaints.objects.create(author=self.user, comment=self.comment)
        self.complaint.save()
        self.complaint2 = Complaints.objects.create(author=self.user, comment=self.comment)
        self.complaint2.save()

    def tearDown(self):
        self.user.delete()
        self.category.delete()

    def test_comparison_data(self):
        self.assertEqual(self.complaint.author, self.user)
        self.assertEqual(self.complaint.comment, self.comment)
        self.assertEqual(self.complaint.comment.author, self.user)
        self.assertFalse(self.complaint.is_reviewed)
