import json
from builtins import print


essentials = (
    "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Phenylalanine", "Threonine", "Tryptophan", "Valine")
#kids_supplement = ("Tyrosine")
kids_essentials = (
    "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Phenylalanine", "Threonine", "Tryptophan", "Valine", "Tyrosine")
cond_essentials = ("Arginine", "Glutamine", "Cysteine", "Glycine", "Proline", "Tyrosine") #Glutamine not present in dataset
# non_essetials = ("Alanine", "Aspartic acid", "Asparagine", "Glutamic acid", "Serine", "Selenocysteine") #Asparagine, Selenocysteine not present

calorific_values = ()

unit_name = "g"

def parse_nutrients(food_list, amino_acids, output_foods):

    current_output_food_nutrients = []
    food_number = 0
    match_number = 0
    found_acids_in_current = 0

    for current_food in food_list:
        nutrients = current_food["foodNutrients"]

        for current_nutrient in nutrients:
            for current_amino in amino_acids:
                if current_nutrient["nutrient"]["name"] == current_amino:
                    if current_nutrient["nutrient"]["unitName"] == unit_name:
                        current_output_food_nutrients.append(current_nutrient["amount"])
                        found_acids_in_current += 1


        if found_acids_in_current == len(amino_acids):
            print(str(match_number), str(food_number), current_food["description"], current_output_food_nutrients)
            add_to_category(output_foods, current_food["foodCategory"]["description"], current_food["description"], current_output_food_nutrients.copy())
            current_output_food_nutrients = []
            match_number += 1

        found_acids_in_current = 0
        food_number += 1

    return output_foods


def add_to_category(categories_dict, key, single_food_description, single_food_nutrients):
    if key not in categories_dict:
        categories_dict[key] = {}

    categories_dict[key][single_food_description] = single_food_nutrients

def print_extraction(categories_dict):
    for current_key, current_value in categories_dict.items():
        print(current_key + ":",  current_value)

    print("Total:", len(categories_dict.keys()))

def print_categories(input_set):
    for current_category, current_number in input_set.items():
        print(current_category + ": " + str(current_number))

#execution code

nutrients_list = kids_essentials

output_file = open("NutrientsList.json", "w")
output_file.write(json.dumps(nutrients_list))
output_file.close()

output_foods = {}

with open("./DataSets/FoodData_Central_sr_legacy_food_json_2021-10-28.json") as food_data_file:
    global_food_data = json.load(food_data_file)
    global_legacy_food_list = global_food_data["SRLegacyFoods"]

output_foods = parse_nutrients(global_legacy_food_list, nutrients_list, output_foods)

with open("./DataSets/FoodData_Central_foundation_food_json_2022-04-28.json") as food_data_file:
    global_food_data = json.load(food_data_file)
    global_foundation_food_list = global_food_data["FoundationFoods"]

output_foods = parse_nutrients(global_foundation_food_list, nutrients_list, output_foods)




#print(json.dumps(output_foods))
output_file = open("ProcessedFoodData.json", "w")
output_file.write(json.dumps(output_foods))
output_file.close()

