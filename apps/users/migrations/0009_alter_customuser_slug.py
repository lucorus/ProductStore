# Generated by Django 5.0.4 on 2024-12-29 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_comment_showing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]