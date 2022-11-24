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
from recommender import knowledge_base

from rest_framework.decorators import api_view
from rest_framework.response import Response

#from amino_json_responder import fill_models_from_fdc_data


#print(os.path.abspath("./../../process_fdc_data/ProcessedFoodData.json"))


class ContainingFoodsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Food.objects.filter(food_category__vegan = True)
    serializer_class = serializers.FoodSerializer

class GetOptimizedMixingRatioViewSet(viewsets.ViewSet):


    def list(self, request, format = None):

        foods = json.loads(request.query_params.get('Foods'))
        age = json.loads(request.query_params.get('Age'))
        weight = json.loads(request.query_params.get('Weight'))

        foods_nutrients = {}
        
        for current_food in foods:
            requested_food_query_set = models.Food.objects.filter(food_name__contains = current_food).order_by(Length('food_name').asc())[:1]
            if len(requested_food_query_set) != 0:
                single_record = requested_food_query_set[0]
                foods_nutrients[single_record.food_name] = single_record.get_nutrients()


        normalized_mixing_ratio, relative_nutrients_matrix, output_keys_list = mixing_ratio_optimizer.optimize_mixing_ratio(list(foods_nutrients.values()), age, weight)

        #response = self.__generate_pure_proportions_output(foods_nutrients, normalized_mixing_ratio)
        response = self.__generate_proportions_relative_nutrients_output(foods_nutrients, output_keys_list, normalized_mixing_ratio, relative_nutrients_matrix)

        return Response(response)

    def __generate_pure_proportions_output(self, foods_nutrients, normalized_mixing_ratio):

        mixing_ratios_dict = {}
        foods_list = list(foods_nutrients.keys())

        for i in range(len(foods_list)):
            mixing_ratios_dict[foods_list[i]] = normalized_mixing_ratio[i]

        return mixing_ratios_dict
            

    def __generate_proportions_relative_nutrients_output(self, foods_nutrients, foods_nutrients_list, normalized_mixing_ratio, relative_nutrients_matrix):
        output_dict = {}
        
        foods_nutrients_keys_list = list(foods_nutrients.keys())
        foods_nutrients_values_list = list(foods_nutrients.values())
        for i in range(len(foods_nutrients_keys_list)):
            proportion_dict = {}
            proportion_dict["Proportion"] = normalized_mixing_ratio[i]
            nutrients_coverage = list(relative_nutrients_matrix[i])
            coverage_dict = {foods_nutrients_list[j]: nutrients_coverage[j] for j in range(len(nutrients_coverage))}          
            proportion_dict["100_g_coverage"] = coverage_dict
            combined_parts_dict = {}
            combined_parts_dict["methionine_part"] = self.__calculate_relative_part(foods_nutrients_values_list[i]["Methionine"], foods_nutrients_values_list[i]["CystEine"])
            combined_parts_dict["phenylalaline_part"] = self.__calculate_relative_part(foods_nutrients_values_list[i]["Phenylalanine"], foods_nutrients_values_list[i]["Tyrosine"])
            proportion_dict["Combined Parts"] = combined_parts_dict
            output_dict[foods_nutrients_keys_list[i]] = proportion_dict

        return output_dict

    def __calculate_relative_part(self, relative_part_of_this, second_in_sum):

        denominator = relative_part_of_this + second_in_sum

        if denominator == 0:
            relative_part = 0.0
        else:
            relative_part = relative_part_of_this / denominator
        return  relative_part

        


class GetNormalizedRequirementsAPIView(APIView):

    def get(self, request, format = None):

        return Response()

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
        response = requested_food_query_set.get_nutrients()
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
        chosen_foods[found_food.food_name] = found_food.get_nutrients()

    return Response(chosen_foods)