# Generated by Django 4.1.2 on 2022-11-25 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amino_json_responder', '0035_complementarypair_food_1_part_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complementarypair',
            old_name='AminoScore',
            new_name='score',
        ),
    ]