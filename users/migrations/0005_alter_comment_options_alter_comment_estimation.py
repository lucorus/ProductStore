# Generated by Django 5.0.4 on 2024-05-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_comment_estimation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='estimation',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='Оценка'),
        ),
    ]
