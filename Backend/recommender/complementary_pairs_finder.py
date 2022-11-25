from amino_json_responder import models
from recommender import mixing_ratio_optimizer
import sys
import time

MIN_NUMBER_OF__OBJECTS_AT_ONCE = 5000

def find_complementary_pairs(category, restriction):

    
    foods_query_set = models.Food.objects.filter(food_category__category_name = category)
    #bizarre_behavior_row = foods_query_set[133]
    number_of_foods = len(foods_query_set)# if len(foods_query_set) < debug_limit else debug_limit
    pairs_list = []

    models.ComplementaryPair.objects.all().delete()
    for i in range(number_of_foods):
        print("Calculating Scores- i: ", str(i))
        if len(pairs_list) >= MIN_NUMBER_OF__OBJECTS_AT_ONCE:
            tic = time.time()
            models.ComplementaryPair.objects.bulk_create(pairs_list)
            toc = time.time()
            print("Bulk create time:", str((toc - tic) * 1000), "for", str(pairs_list.__len__()), "objects")
            pairs_list = []

        for j in range(i + 1, number_of_foods):
            #print("j: ", str(j))
            loop_start_time  = time.time()
            foods_list = [foods_query_set[i], foods_query_set[j]]
            foods_nutrients_lists = []
            for current_food in foods_list:
                foods_nutrients_lists.append(current_food.get_nutrients())
            tic = time.time()
            normalized_mixing_ratio, relative_nutrients_matrix, output_keys_list, score = mixing_ratio_optimizer.optimize_mixing_ratio_for_adult_who_recommendation(foods_nutrients_lists)
            toc = time.time()
            #if (mixing_ratio_optimizer.is_mixed_better_than_all_single_foods(normalized_mixing_ratio, relative_nutrients_matrix)):
            if (0 not in normalized_mixing_ratio):
                #print("Opt Time: :", str((toc - tic) * 1000))
                current_pair = models.ComplementaryPair()
                current_pair.food_1 = foods_list[0]
                current_pair.food_2 = foods_list[1]
                current_pair.food_1_fdc_id = foods_list[0].fdc_id
                current_pair.food_2_fdc_id = foods_list[1].fdc_id
                current_pair.score = score
                current_pair.food_1_part = normalized_mixing_ratio[0]
                current_pair.food_2_part = normalized_mixing_ratio[1]
                tic = time.time()
                #current_pair.save(current_pair)
                pairs_list.append(current_pair)
                toc = time.time()
                #print("Save Time: :", str((toc - tic) * 1000))
                tic = time.time()
                loop_stop_time  = time.time()
                #print("Loop Time: ", (loop_stop_time - loop_start_time) * 1000)

    models.ComplementaryPair.objects.bulk_create(pairs_list)
        


find_complementary_pairs("Vegetables and Vegetable Products", "vegan")
