from amino_json_responder import models
import os
import json
from builtins import print
import numpy as np

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


amino_acids_model_fields_to_fdc_map = {
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
    "CystEine": findCystEine
}

additional_nutrients_model_fields_to_fdc_map = {
    "IsTrueCysteine": findTrueCysteine,
    "TotalProtein": "Protein",
    "TotalFat": "Total lipid (fat)",
    "TotalCarbohydrates": findCarbohydrates,
    "TotalEnergy": findEnergy
}


def parse_nutrients(food_list, amino_acids_map, additional_nutrients_map):

    food_number = 0
    match_number = 0

    found_all_searched_nutrients = False

    model_rows_list = []
    found_amino_acids_dict = {}
    found_additional_nutrients_dict = {}
    n_found_amino_acids = 0
    n_found_additional_nutrients = 0

    for current_food in food_list:
        nutrients = current_food["foodNutrients"]
        for current_nutrient in nutrients:
            n_found_amino_acids += parse_single_nutrient(current_nutrient, amino_acids_map, found_amino_acids_dict)
            n_found_additional_nutrients += parse_single_nutrient(current_nutrient, additional_nutrients_map, found_additional_nutrients_dict)
            found_all_searched_nutrients = n_found_amino_acids + n_found_additional_nutrients == len(amino_acids_map) + len(additional_nutrients_map)

        if found_all_searched_nutrients:
            
            add_model_to_row_list(model_rows_list, current_food, found_amino_acids_dict, found_additional_nutrients_dict)

            print(str(match_number), str(food_number), current_food["description"])
            match_number += 1
            
        n_found_amino_acids = 0
        n_found_additional_nutrients = 0
        found_amino_acids_dict = {}
        found_additional_nutrients_dict = {}
        food_number += 1
        found_all_searched_nutrients = False

    models.Food.objects.bulk_create(model_rows_list)



def add_model_to_row_list(model_rows_list, current_food, found_amino_acids_dict, found_additional_nutrients_dict):

    current_row_model = models.Food()
    append_normalized_amounts(found_amino_acids_dict)
    current_row_model.set_dict_to_fields(found_amino_acids_dict)
    current_row_model.set_dict_to_fields(found_additional_nutrients_dict)

    current_row_model.food_name = current_food["description"]
    current_row_model.fdc_id = current_food["fdcId"]
    category_name = current_food["foodCategory"]["description"]
    category = add_to_category(category_name)
    current_row_model.food_category = category
    model_rows_list.append(current_row_model)


def parse_single_nutrient(single_nutrient, model_fields_map, found_nutrients_dict):


    found_fields_in_current = 0

    for current_model_field, current_db_string_or_function in model_fields_map.items():
        value_to_set = 0
        if type(current_db_string_or_function) is str:
            found, value_to_set = findStringDefaultFunction(single_nutrient, current_db_string_or_function)
        else:
            found, value_to_set = current_db_string_or_function(single_nutrient) 
        if (found):
            if(found_nutrients_dict.get(current_model_field) == None):
                found_fields_in_current += 1
                found_nutrients_dict[current_model_field] = value_to_set

    return found_fields_in_current
             



def append_normalized_amounts(nutrients_dict):
    
    #calculate relative values
    nutrients_array = np.array(list(nutrients_dict.values()))
    values_sum = nutrients_array.sum()

    if values_sum != 0:
        nutrients_array /= values_sum

    relative_keys_list = []

    for current_key in nutrients_dict.keys():
        relative_keys_list.append("Relative" + current_key)

    nutrients_dict.update(zip(relative_keys_list, nutrients_array))
    nutrients_dict["AminoAcidsSum"] = values_sum

    return nutrients_dict



def fill_models_with_fdc_data(root_key, rel_path):
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, rel_path)) as food_data_file:
        global_food_data = json.load(food_data_file)
        food_list = global_food_data[root_key]
    parse_nutrients(food_list, amino_acids_model_fields_to_fdc_map, additional_nutrients_model_fields_to_fdc_map)
    

def clear_models():
    models.Food.objects.all().delete()
    models.FoodCategory.objects.all().delete()

clear_models()
fill_models_with_fdc_data("FoundationFoods", "../process_fdc_data/DataSets/FoodData_Central_foundation_food_json_2022-10-28.json")
fill_models_with_fdc_data("SRLegacyFoods", "../process_fdc_data/DataSets/FoodData_Central_sr_legacy_food_json_2021-10-28.json")