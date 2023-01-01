# Generated by Django 4.1.2 on 2022-11-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amino_json_responder', '0016_food_id_remove_food_histidine_food_histidine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='Histidine',
            field=models.ManyToManyField(related_name='%(class)s_requests_created', to='amino_json_responder.nutrient'),
        ),
        migrations.RemoveField(
            model_name='food',
            name='Isoleucine',
        ),
        migrations.AddField(
            model_name='food',
            name='Isoleucine',
            field=models.ManyToManyField(related_name='%(class)s_reques', to='amino_json_responder.nutrient'),
        ),
    ]