from secrets import choice
from django.http import HttpResponse
import json
#import os
import random
from django.db.models.functions import Length
from amino_json_responder import models
from amino_json_responder import serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from recommender import mixing_ratio_optimizer

from rest_framework.decorators import api_view
from rest_framework.response import Response

#from amino_json_responder import fill_models

#print(os.path.abspath("./../../process_fdc_data/ProcessedFoodData.json"))


class ContainingFoodsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Food.objects.filter(food_category__vegan = True)
    serializer_class = serializers.FoodSerializer

class GetOptimizedMixingRatioAPIView(APIView):

    def get(self, request, format = None):

        foods = json.loads(request.query_params.get('Foods'))
        age = json.loads(request.query_params.get('Age'))
        weight = json.loads(request.query_params.get('Weight'))

        foods_nutrients = {}
        
        for current_food in foods:
            requested_food_query_set = models.Food.objects.filter(food_name__contains = current_food).order_by(Length('food_name').asc())[:1]
            single_record = requested_food_query_set[0]
            foods_nutrients[single_record.food_name] = single_record.get_nutrients_values()

        normalized_mixing_ratio = mixing_ratio_optimizer.optimize_mixing_ratio(list(foods_nutrients.values()), age, weight)

        mixing_ratios_dict = {}

        foods_list = list(foods_nutrients.keys())
        for i in range(len(foods_list)):
            mixing_ratios_dict[foods_list[i]] = normalized_mixing_ratio[i]

        return Response(mixing_ratios_dict)


@api_view()
def get_nutrients_list(request):

    return Response(models.Food.get_nutrients_keys())

@api_view()
def get_foods(request, restriction):

    found_foods = []

    if restriction == "none":
        foods_query_set = models.Food.objects.all()
    if restriction == "vegetarian":
        foods_query_set = models.Food.objects.filter(food_category__vegetarian = True)
    if restriction == "vegan":
        foods_query_set = models.Food.objects.filter(food_category__vegan = True)

    for current_food in foods_query_set:

        found_foods.append(current_food.food_name)

    return Response(found_foods)


@api_view()
def get_containing_foods(request, searched_food):

    foods_query_set = models.Food.objects.filter(food_category__vegan = True).filter(food_name__contains = searched_food)
    found_foods = []

    for current_food in foods_query_set:
        found_foods.append(current_food.food_name)

    return Response(found_foods)

@api_view()
def get_nutrients_info(request, exact_food_key_string):
    
    try:
        requested_food_query_set = models.Food.objects.get(food_name = exact_food_key_string)
        response = requested_food_query_set.get_nutrients_values()
    except(models.Food.DoesNotExist):
        response = "key not found"

    return Response(response)

@api_view()
def get_recommended_foods(request):

    input_nutrients =  json.loads(request.query_params.get('Nutrients'))

    chosen_foods = {}
    foods_query_set = models.Food.objects.filter(food_category__vegan = True)

    for i in range(5):
        found_food = random.choice(foods_query_set)
        chosen_foods[found_food.food_name] = found_food.get_nutrients_values()

    return Response(chosen_foods)