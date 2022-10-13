import json
from builtins import print


essentials = (
    "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Phenylalanine", "Threonine", "Tryptophan", "Valine")
#kids_supplement = ("Tyrosine")
kids_essentials = (
    "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine", "Phenylalanine", "Threonine", "Tryptophan", "Valine", "Tyrosine")
cond_essentials = ("Arginine", "Glutamine", "Cysteine", "Glycine", "Proline", "Tyrosine") #Glutamine not present in dataset
# non_essetials = ("Alanine", "Aspartic acid", "Asparagine", "Glutamic acid", "Serine", "Selenocysteine") #Asparagine, Selenocysteine not present


def parse_nutrients(food_list, amino_acids, input_foods, input_categories):

    current_output_food_aminos = []
    food_number = 0
    match_number = 0
    found_acids_in_current = 0

    for current_food in food_list:
        nutrients = current_food["foodNutrients"]

        for current_nutrient in nutrients:
            for current_amino in amino_acids:
                if current_nutrient["nutrient"]["name"] == current_amino:
                    current_output_food_aminos.append(current_nutrient["amount"])
                    found_acids_in_current += 1


        if found_acids_in_current == len(amino_acids):
            #print(str(match_number), str(food_number), current_food["description"], current_output_food_aminos)
            if current_food["foodCategory"]["description"] == "Legumes and Legume Products":
                output_foods[current_food["description"]] = current_output_food_aminos.copy()
                inc_dict(found_categories, current_food["foodCategory"]["description"])
            current_output_food_aminos = []
            match_number += 1

        found_acids_in_current = 0
        food_number += 1

    return output_foods, found_categories


def inc_dict(input_dict, key):
    if key in input_dict:
        input_dict[key] += 1
    else:
        input_dict[key] = 1


def print_extraction(input_dict):
    for current_key, current_value in input_dict.items():
        print(current_key + ":",  current_value)

    print("Total:", len(input_dict.keys()))

def print_categories(input_set):
    for current_category, current_number in input_set.items():
        print(current_category + ": " + str(current_number))




output_foods = {}
found_categories = {}

# with open("./DataSets/FoodData_Central_sr_legacy_food_json_2021-10-28.json") as food_data_file:
#     global_food_data = json.load(food_data_file)
#     global_legacy_food_list = global_food_data["SRLegacyFoods"]
#
# output_foods, found_categories = parse_nutrients(global_legacy_food_list, kids_essentials, output_foods, found_categories)

with open("./DataSets/FoodData_Central_foundation_food_json_2022-04-28.json") as food_data_file:
    global_food_data = json.load(food_data_file)
    global_foundation_food_list = global_food_data["FoundationFoods"]

output_foods, found_categories = parse_nutrients(global_foundation_food_list, kids_essentials, output_foods, found_categories)



print_categories(found_categories)
print_extraction(output_foods)

print(json.dumps(output_foods))
output_file = open("DemoResponse.json", "w")
output_file.write(json.dumps(output_foods))
output_file.close()
