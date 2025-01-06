# Generated by Django 5.0.4 on 2024-05-19 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_comment_estimation'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='access_write_comments',
            field=models.BooleanField(default=True, verbose_name='Пользователь может писать комментарии?'),
        ),
        migrations.CreateModel(
            name='Complaints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_reviewed', models.BooleanField(default=False, verbose_name='Рассмотрено?')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_complaints', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='users.comment', verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Жалоба',
                'verbose_name_plural': 'Жалобы',
                'ordering': ['-id'],
            },
        ),
    ]