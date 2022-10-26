from django.db import models


# Create your models here.

refresh_all_models = True

class FoodCategory(models.Model):
    category_name = models.CharField(max_length = 80)

    def __str__(self):
        return self.category_name

class Food(models.Model):
    food_name = models.CharField(max_length = 80)
    Histidine = models.FloatField()
    Isoleucine = models.FloatField()
    Leucine = models.FloatField()
    Lysine = models.FloatField()
    Methionine = models.FloatField()
    Phenylalanine = models.FloatField()
    Threonine = models.FloatField()
    Tryptophan = models.FloatField()
    Valine = models.FloatField()
    Tyrosine = models.FloatField()
    food_category = models.ForeignKey(FoodCategory, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.food_name


