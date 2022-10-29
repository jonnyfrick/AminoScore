from secrets import choice
from django.http import HttpResponse
import json
#import os
import random
from amino_json_responder import models

#from amino_json_responder import fill_models

#print(os.path.abspath("./../../process_fdc_data/ProcessedFoodData.json"))

def get_nutrients_list(request):

    return HttpResponse(json.dumps(models.Food.get_nutrients_keys()))
    
def get_containing_foods(request, searched_food):

    foods_query_set = models.Food.objects.filter(food_category__vegan = True).filter(food_name__contains = searched_food)
    found_foods = []

    for current_food in foods_query_set:
        found_foods.append(current_food.food_name)

    return HttpResponse(json.dumps(found_foods))

def get_nutrients_info(request, exact_food_key_string):
    
    try:
        requested_food_query_set = models.Food.objects.get(food_name = exact_food_key_string)
        response = requested_food_query_set.get_nutrients_values()
    except(models.Food.DoesNotExist):
        response = "key not found"

    return HttpResponse(json.dumps(response))

def get_recommended_foods(request, url_param):

    chosen_foods = {}
    foods_query_set = models.Food.objects.filter(food_category__vegan = True)

    for i in range(5):
        found_food = random.choice(foods_query_set)
        chosen_foods[found_food.food_name] = found_food.get_nutrients_values()

    return HttpResponse(json.dumps(chosen_foods))