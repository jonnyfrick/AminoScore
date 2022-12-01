from django.db import models
from django.forms.models import model_to_dict
import numpy as np

# Create your models here.

food_model_header_fields = 4
n_aminos = 11


class FoodCategory(models.Model):
    category_name = models.CharField(max_length = 80)
    vegan = models.BooleanField(default = False)
    vegetarian = models.BooleanField(default = False)

    def __str__(self):
        return self.category_name


class Food(models.Model):
    food_category = models.ForeignKey(FoodCategory, null = True, on_delete = models.SET_NULL)
    food_name = models.CharField(max_length = 80)
    fdc_id = models.IntegerField(default = 0)
    
    Histidine = models.FloatField(default = 0)
    Isoleucine = models.FloatField(default = 0)
    Leucine = models.FloatField(default = 0)
    Lysine = models.FloatField(default = 0)
    Methionine = models.FloatField(default = 0)
    Phenylalanine = models.FloatField(default = 0)
    Threonine = models.FloatField(default = 0)
    Tryptophan = models.FloatField(default = 0)
    Valine = models.FloatField(default = 0)
    Tyrosine = models.FloatField(default = 0)
    CystEine = models.FloatField(default = 0)
    IsTrueCysteine = models.BooleanField(default = False)

    TotalProtein = models.FloatField(default = 0)
    TotalFat = models.FloatField(default = 0)
    TotalCarbohydrates = models.FloatField(default = 0)

    TotalEnergy = models.FloatField(default = 0)

    RelativeHistidine = models.FloatField(default = 0)
    RelativeIsoleucine = models.FloatField(default = 0)
    RelativeLeucine = models.FloatField(default = 0)
    RelativeLysine = models.FloatField(default = 0)
    RelativeMethionine = models.FloatField(default = 0)
    RelativePhenylalanine = models.FloatField(default = 0)
    RelativeThreonine = models.FloatField(default = 0)
    RelativeTryptophan = models.FloatField(default = 0)
    RelativeValine = models.FloatField(default = 0)
    RelativeTyrosine = models.FloatField(default = 0)
    RelativeCystEine = models.FloatField(default = 0)
    AminoAcidsSum = models.FloatField(default = 0)


    def __str__(self):
        return self.food_name

    def set_dict_to_fields(self, input_dict):

        for current_model_field, value_to_set in input_dict.items():
            self.__setattr__(current_model_field, value_to_set) 


    @staticmethod
    def get_nutrients_keys():

        nutrients_keys_list = list(model_to_dict(Food).keys())
        return nutrients_keys_list[food_model_header_fields:]

    def get_nutrients(self):
        nutrients_dict = model_to_dict(self)
        for current_key_to_drop in list(nutrients_dict.keys())[:food_model_header_fields]:
            nutrients_dict.pop(current_key_to_drop, None)
        return nutrients_dict

    def get_amino_acids_dict(self):
        nutrients_dict = self.get_nutrients()

        sum = nutrients_dict["AminoAcidsSum"]
        for current_key_to_drop in list(nutrients_dict.keys())[n_aminos:]:
            nutrients_dict.pop(current_key_to_drop, None)

        normalized_array = np.array(list(nutrients_dict.values()))
        absolute_content_array = normalized_array * sum

        nutrients_dict.update(zip(nutrients_dict.keys(), absolute_content_array))
        return nutrients_dict


    def get_nutrients_values(self):
        
        food_dict = model_to_dict(self)
        nutrients_values_list = list(food_dict.values())
        return nutrients_values_list[food_model_header_fields:]

    def get_name_nutrients_dict(self):

        name_nutrients_dict  = {self.food_name: self.get_nutrients_values()}
        return name_nutrients_dict

    


class ComplementaryPair(models.Model):
    food_1 = models.ForeignKey(Food, related_name='food_1', null = True, on_delete = models.SET_NULL)
    food_2 = models.ForeignKey(Food, related_name='food_2', null = True, on_delete = models.SET_NULL)
    food_1_fdc_id = models.IntegerField(default = 0) #restoration capability
    food_2_fdc_id = models.IntegerField(default = 0) #restoration capability
    score = models.FloatField(default = 0)
    food_1_part = models.FloatField(default = 0)
    food_2_part = models.FloatField(default = 0)

    def __str__(self):
        return self.food_1.food_name + '+' + self.food_2.food_name + ': ' + str(self.score)



    




