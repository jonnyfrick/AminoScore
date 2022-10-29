from django.db import models
from django.forms.models import model_to_dict

# Create your models here.

food_model_header_fields = 3


class FoodCategory(models.Model):
    category_name = models.CharField(max_length = 80)
    vegan = models.BooleanField(default = False)
    vegetarian = models.BooleanField(default = False)

    def __str__(self):
        return self.category_name


class Food(models.Model):
    food_category = models.ForeignKey(FoodCategory, null = True, on_delete = models.SET_NULL)
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

    def __str__(self):
        return self.food_name

    @staticmethod
    def get_nutrients_keys():

        nutrients_keys_list = list(model_to_dict(Food).keys())
        return nutrients_keys_list[food_model_header_fields:]

    def get_nutrients_values(self):
        
        food_dict = model_to_dict(self)
        nutrients_values_list = list(food_dict.values())
        return nutrients_values_list[food_model_header_fields:]

    def get_name_nutrients_dict(self):

        name_nutrients_dict  = {self.food_name: self.get_nutrients_values()}
        return name_nutrients_dict
    



