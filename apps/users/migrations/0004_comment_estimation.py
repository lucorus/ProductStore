# Generated by Django 5.0.4 on 2024-05-15 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='estimation',
            field=models.PositiveSmallIntegerField(default=5, verbose_name='Оценка'),
        ),
    ]