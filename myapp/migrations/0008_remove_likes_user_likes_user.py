# Generated by Django 4.2.1 on 2023-09-24 06:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0007_remove_commentuser_email_remove_commentuser_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='user',
        ),
        migrations.AddField(
            model_name='likes',
            name='user',
            field=models.ManyToManyField(related_name='like_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
