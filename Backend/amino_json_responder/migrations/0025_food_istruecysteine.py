# Generated by Django 4.1.2 on 2022-11-19 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amino_json_responder', '0024_food_totalcarbohydrates_food_totalenergy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='IsTrueCysteine',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]