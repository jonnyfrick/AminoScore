# Generated by Django 4.1.2 on 2022-10-29 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amino_json_responder', '0010_foodcategory_vegan_foodcategory_vegetarian'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='food_category',
        ),
    ]
