from secrets import choice
from django.http import HttpResponse
import json
#import os
import random

#print(os.path.abspath("./../../process_fdc_data/ProcessedFoodData.json"))

category = "Vegetables and Vegetable Products"



with open("./process_fdc_data/ProcessedFoodData.json") as food_data_file:
    global_food_data = json.load(food_data_file)

with open("./process_fdc_data/NutrientsList.json") as nutrients_list_file:
    global_nutrients_list = json.load(nutrients_list_file)

def get_nutrients_list(request):

    return HttpResponse(json.dumps(global_nutrients_list))
    
def get_containing_foods(request, searched_food):

    one_category = global_food_data[category]
    found_foods = []
    output = "nothing found"

    for current_food in one_category.keys():
        if searched_food in current_food:
            found_foods.append(current_food)
            output = found_foods
    return HttpResponse(json.dumps(output))

def get_nutrients_info(request, exact_food_key_string):

    one_category = global_food_data[category]

    output = "key not found"
    return HttpResponse(json.dumps(one_category[exact_food_key_string]))

def get_recommended_foods(request, url_param):

    one_category = global_food_data[category]

    choson_foods = {}

    for i in range(5):
        found_nutrient_key = random.choice(list(one_category.keys()))
        found_nutrient_value = one_category[found_nutrient_key]
        choson_foods[found_nutrient_key] = found_nutrient_value

    return HttpResponse(json.dumps(choson_foods))