from django.forms import ModelForm
from . import models


class CategoryForm(ModelForm):
    class Meta:
        model = models.Category
        fields = ['title', 'image']


class SubCategoryForm(ModelForm):
    class Meta:
        model = models.SubCategory
        fields = ['title', 'category', 'image']


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['title', 'price', 'discount', 'photo', 'subcategory', 'showing']

