# Generated by Django 4.1.2 on 2022-10-29 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amino_json_responder', '0011_remove_food_food_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='food_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='amino_json_responder.foodcategory'),
        ),
    ]