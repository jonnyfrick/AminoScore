from lzma import FILTER_LZMA1
from amino_json_responder import models
import json

fill_database = True

vegan_keywords = ["baked", "vegetable", "fruit", "legume", "cereal", "spice", "herb", "grains", "pasta"]
vegetarian_keywords =["diary", "milk", "egg"]

with open("./process_fdc_data/ProcessedFoodData.json") as food_data_file:
    global_food_data = json.load(food_data_file)

with open("./process_fdc_data/NutrientsList.json") as nutrients_list_file:
    global_nutrients_list = json.load(nutrients_list_file)

def fulfills_diet(diet_keywords, category):

    fulfills_return_bool = False

    for current_keyword in diet_keywords:
        if current_keyword.lower() in category.lower():
            fulfills_return_bool = True
            break

    return fulfills_return_bool


def fill_all_models(output_foods):

    for current_category_key, current_category_value in output_foods.items():

        is_vegetarian = False
        is_vegan = False

        if fulfills_diet(vegetarian_keywords, current_category_key):
            is_vegetarian = True

        if fulfills_diet(vegan_keywords, current_category_key):
            is_vegetarian = True
            is_vegan = True

        current_food_category_entry = models.FoodCategory(category_name = current_category_key, vegan = is_vegan, vegetarian = is_vegetarian)
        current_food_category_entry.save()
        print("adding: " + current_category_key)

        for current_food_key, curren_food_nutrients in current_category_value.items():
            current_food_entry = models.Food(
                food_name = current_food_key,
                Histidine = curren_food_nutrients[0],
                Isoleucine = curren_food_nutrients[1],
                Leucine = curren_food_nutrients[2],
                Lysine = curren_food_nutrients[3],
                Methionine = curren_food_nutrients[4],
                Phenylalanine = curren_food_nutrients[5],
                Threonine = curren_food_nutrients[6],
                Tryptophan = curren_food_nutrients[7],
                Valine = curren_food_nutrients[8],
                Tyrosine = curren_food_nutrients[9],
                food_category = current_food_category_entry)
            current_food_entry.save()


def refresh_all_models(output_foods):
    models.Food.objects.all().delete()
    models.FoodCategory.objects.all().delete()

    if fill_database:
        fill_all_models(output_foods)


#execution code
with open("./process_fdc_data/ProcessedFoodData.json") as food_data_file:
    global_food_data = json.load(food_data_file)

refresh_all_models(global_food_data)