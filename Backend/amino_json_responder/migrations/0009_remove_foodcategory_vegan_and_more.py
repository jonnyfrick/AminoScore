# Generated by Django 4.1.2 on 2022-10-27 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amino_json_responder', '0008_foodcategory_vegan_foodcategory_vegetarian'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodcategory',
            name='vegan',
        ),
        migrations.RemoveField(
            model_name='foodcategory',
            name='vegetarian',
        ),
    ]