from amino_json_responder import models
import json


with open("./process_fdc_data/ProcessedFoodData.json") as food_data_file:
    global_food_data = json.load(food_data_file)

with open("./process_fdc_data/NutrientsList.json") as nutrients_list_file:
    global_nutrients_list = json.load(nutrients_list_file)


def refresh_all_models(output_foods):
    models.Food.objects.all().delete()
    models.FoodCategory.objects.all().delete()

    for current_category_key, current_category_value in output_foods.items():
        current_food_category_entry = models.FoodCategory(category_name = current_category_key)
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


#execution code
with open("./process_fdc_data/ProcessedFoodData.json") as food_data_file:
    global_food_data = json.load(food_data_file)

refresh_all_models(global_food_data)