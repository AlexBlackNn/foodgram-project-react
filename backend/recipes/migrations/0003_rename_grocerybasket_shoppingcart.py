# Generated by Django 4.1.1 on 2022-09-08 15:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GroceryBasket',
            new_name='ShoppingCart',
        ),
    ]
