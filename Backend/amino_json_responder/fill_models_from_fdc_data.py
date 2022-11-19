from amino_json_responder import models
import os
import json
from builtins import print

default_unit_name = "g"
vegan_keywords = ["baked", "vegetable", "fruit", "legume", "cereal", "spice", "herb", "grains", "pasta"]
vegetarian_keywords =["diary", "milk", "egg"]

def fulfills_diet(diet_keywords, category):

    fulfills_return_bool = False

    for current_keyword in diet_keywords:
        if current_keyword.lower() in category.lower():
            fulfills_return_bool = True
            break

    return fulfills_return_bool

def add_to_category(category_name):
    try:
        category = models.FoodCategory.objects.get(category_name = category_name)
    except (models.FoodCategory.DoesNotExist):
        is_vegetarian = False
        is_vegan = False

        if fulfills_diet(vegetarian_keywords, category_name):
            is_vegetarian = True

        if fulfills_diet(vegan_keywords, category_name):
            is_vegetarian = True
            is_vegan = True
        category = models.FoodCategory(category_name = category_name, vegan = is_vegan, vegetarian = is_vegetarian)
        category.save()

    return category

cyst_e_ine_variants = ("Cysteine", "Cystine")

def findCystEine(current_nutrient):
    found = False
    value_to_set = -1

    for current_variant in cyst_e_ine_variants:
        found, value_to_set = findStringDefaultFunction(current_nutrient, current_variant)
        if found:
            break

    return found, value_to_set


def findTrueCysteine(current_nutrient):

    found = False
    value_to_set = False

    for current_variant in cyst_e_ine_variants:
        found, default_function_output_value = findStringDefaultFunction(current_nutrient, current_variant)
        if found:
            if current_variant == "Cysteine":
                value_to_set = True
            else:
                value_to_set = False
            break

    return found, value_to_set


def findCarbohydrates(current_nutrient):

    #strategy for buffering value needed if more than one value should be taken into account
    find_carbohydrates_entries = ("Carbohydrate, by difference",) #"Carbohydrate, by summation")
    found = False
    value_to_set = -1

    for current_variant in find_carbohydrates_entries:
        found, value_to_set = findStringDefaultFunction(current_nutrient, current_variant)

    return found, value_to_set


def findEnergy(current_nutrient):

    energy_strings = ("Energy", "Energy (Atwater General Factors)")
    found = False
    value_to_set = -1

    for current_variant in energy_strings:
        if current_nutrient["nutrient"]["name"] == current_variant:

            unit_name = current_nutrient["nutrient"]["unitName"]
            if  unit_name == "kcal":
                value_to_set = current_nutrient["amount"]
                found = True

            elif unit_name == "kJ":
                value_to_set = current_nutrient["amount"] / 4.184
                found = True

    return found, value_to_set


def findStringDefaultFunction(current_nutrient, match_string):
    found = False
    value_to_set = -1
    if current_nutrient["nutrient"]["name"] == match_string:
        if current_nutrient["nutrient"]["unitName"] == default_unit_name:
            value_to_set = current_nutrient["amount"]
            found = True

    return found, value_to_set


model_fields_to_fdc_map = {
    "Histidine": "Histidine",
    "Isoleucine": "Isoleucine",
    "Leucine": "Leucine",
    "Lysine": "Lysine",
    "Methionine": "Methionine",
    "Phenylalanine": "Phenylalanine",
    "Threonine": "Threonine",
    "Tryptophan": "Tryptophan",
    "Valine": "Valine",
    "Tyrosine": "Tyrosine",
    "CystEine": findCystEine,
    "IsTrueCysteine": findTrueCysteine,
    "TotalProtein": "Protein",
    "TotalFat": "Total lipid (fat)",
    "TotalCarbohydrates": findCarbohydrates,
    "TotalEnergy": findEnergy
}


def parse_nutrients(food_list, model_fields_map):

    food_number = 0
    match_number = 0
    found_fields_in_current = 0
    found = False

    for current_food in food_list:
        nutrients = current_food["foodNutrients"]
        current_row_model = models.Food()
        for current_nutrient in nutrients:
            for current_model_field, current_db_string_or_function in model_fields_map.items():
                value_to_set = 0
                if type(current_db_string_or_function) is str:
                    found, value_to_set = findStringDefaultFunction(current_nutrient, current_db_string_or_function)
                else:
                    found, value_to_set = current_db_string_or_function(current_nutrient)

                if (found):
                    if(current_row_model.__getattribute__(current_model_field) == 0):
                        found_fields_in_current += 1
                        current_row_model.__setattr__(current_model_field, value_to_set)

        if found_fields_in_current == len(model_fields_map):
            print(str(match_number), str(food_number),
                  current_food["description"])
            current_row_model.food_name = current_food["description"]
            category_name = current_food["foodCategory"]["description"]
            category = add_to_category(category_name)
            current_row_model.food_category = category
            current_row_model.save()
            match_number += 1

        found_fields_in_current = 0
        food_number += 1
        found = False


script_dir = os.path.dirname(__file__)
rel_path = "../process_fdc_data/DataSets/FoodData_Central_foundation_food_json_2022-10-28.json"
with open(os.path.join(script_dir, rel_path)) as food_data_file:
    global_food_data = json.load(food_data_file)
    global_foundation_food_list = global_food_data["FoundationFoods"]

rel_path = "../process_fdc_data/DataSets/FoodData_Central_sr_legacy_food_json_2021-10-28.json"
with open(os.path.join(script_dir, rel_path)) as food_data_file:
    global_food_data = json.load(food_data_file)
    global_legacy_food_list = global_food_data["SRLegacyFoods"]


def refresh_all_models():
    models.Food.objects.all().delete()
    models.FoodCategory.objects.all().delete()

# refresh_all_models()
# parse_nutrients(global_foundation_food_list, model_fields_to_fdc_map)
# parse_nutrients(global_legacy_food_list, model_fields_to_fdc_map)