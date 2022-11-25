from amino_json_responder import models
from recommender import mixing_ratio_optimizer
import sys
import time
#from multiprocessing import Process
import multiprocessing
import os

MIN_NUMBER_OF_OBJECTS_AT_ONCE = 5000

complementary_pairs_model_lock = multiprocessing.Lock()
print_lock = multiprocessing.Lock()

def locked_print(*args):
    print_lock.acquire()
    print(*args)
    print_lock.release()

def locked_model_write(pairs_list):
    tic = time.time()
    complementary_pairs_model_lock.acquire()
    models.ComplementaryPair.objects.bulk_create(pairs_list)
    complementary_pairs_model_lock.release()
    toc = time.time()
    locked_print("Bulk create time:", str((toc - tic) * 1000), "for", str(pairs_list.__len__()), "objects")


def find_complementary_pairs(category, restriction):

    over_all_time_stamp = time.time()
    models.ComplementaryPair.objects.all().delete()

    foods_query_set = models.Food.objects.filter(food_category__category_name = category)
    number_of_foods = len(foods_query_set)# if len(foods_query_set) < debug_limit else debug_limit
    number_of_cpus = os.cpu_count()



    range_indices =  calculate_split_indices(number_of_foods, number_of_cpus)


    worker_processes = []
    for current_process_number in range(number_of_cpus):
        current_process = multiprocessing.Process(
            target = find_complementary_pairs_worker,
            args = (range_indices[current_process_number], range_indices[current_process_number + 1], foods_query_set))
        worker_processes.append(current_process)
        current_process.start()

    for current_process in worker_processes:
        current_process.join()

    locked_print("find complementary pairs time: ", str(time.time() - over_all_time_stamp))



def calculate_split_indices(number_of_foods, number_of_cpus):

    inner_loop_iterations = number_of_foods - 1
    estimated_overall_iterations = number_of_foods * number_of_foods / 2
    estimated_iterations_per_cpu = estimated_overall_iterations / number_of_cpus

    range_indices = [0]
    done_iterations = 0
    outer_loop_iteration = 0
    current_split_index = 0

    for current_inner_loop_iterations in range(inner_loop_iterations, 1, -1):
        outer_loop_iteration += 1 
        done_iterations += current_inner_loop_iterations

        if(done_iterations > estimated_iterations_per_cpu * (current_split_index + 1)):
            current_split_index += 1
            range_indices.append(outer_loop_iteration)
            if current_split_index == number_of_cpus:
                break

    range_indices.append(number_of_foods)
    return range_indices


     
def find_complementary_pairs_worker(start_ind, stop_ind, foods_query_set):
    pairs_list = []
    number_of_foods = len(foods_query_set)
    for i in range(start_ind, stop_ind):

        locked_print(str(os. getpid()), "Calculating Scores- i: ", str(i))

        if len(pairs_list) >= MIN_NUMBER_OF_OBJECTS_AT_ONCE:
            locked_model_write(pairs_list)
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

    locked_model_write(pairs_list)


find_complementary_pairs("Vegetables and Vegetable Products", "vegan")
