# Generated by Django 4.1.2 on 2022-10-26 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amino_json_responder', '0004_rename_category_id_food_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='category',
            new_name='food_category',
        ),
    ]