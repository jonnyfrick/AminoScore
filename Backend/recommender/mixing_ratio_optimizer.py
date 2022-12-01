
#from recommender import NutrientsPattern
import numpy as np #jax.numpy for CUDA gpu support- refactoring to immutable jax arrays necessary
from scipy.optimize import minimize, Bounds
from recommender import knowledge_base
import random
import time


MAX_OPTIMIZATION_FACTOR = 10
#PROPORTION_SIGNIFICANCE_LEVEL = 0.01

#@njit
def set_initial_values(relative_nutrients_matrix):
    x0 = np.ones(len(relative_nutrients_matrix))
    
    for i in range(len(x0)):
        over_all_contribution_value = sum(relative_nutrients_matrix[i]) 
        if over_all_contribution_value == 0.0:
            x0[i] = 0
        else:
            x0[i] = 1 / over_all_contribution_value
    #x0 = np.random.rand(len(relative_nutrients_matrix))
    return x0


def optimize_mixing_ratio_for_person_who_recommendation(food_nutrients_dicts, age, weight):


    #if accept who recommended summation
    nutrients_lists = knowledge_base.calculate_who_patterns(food_nutrients_dicts)

    nutrients_matrix = np.array(nutrients_lists)
    #print(nutrients_matrix)

    relative_nutrients_matrix = knowledge_base.calculate_normalized_intake(nutrients_matrix, age, weight)
    #print(relative_nutrients_matrix)

    return optimize_mixing_ratio(relative_nutrients_matrix)


def optimize_mixing_ratio_for_adult_who_recommendation(food_nutrients_dicts):


    #if accept who recommended summation
    nutrients_lists = knowledge_base.calculate_who_patterns(food_nutrients_dicts)

    nutrients_matrix = np.array(nutrients_lists)
    #print(nutrients_matrix)

    relative_nutrients_matrix = knowledge_base.calculate_adult_normalized_intake_per_kg_mg(nutrients_matrix)
    #print(relative_nutrients_matrix)

    return optimize_mixing_ratio(relative_nutrients_matrix)

def fast_two_ingredients_minimize(criterion, x0, relative_nutrients_matrix, bounds):

    return

def optimize_mixing_ratio(relative_nutrients_matrix):


    x0 = set_initial_values(relative_nutrients_matrix)
    mix_is_better, first_better_than_mixed_ind = is_mixed_better_than_all_single_foods(x0, relative_nutrients_matrix)
    
    if False: #mix_is_better:
        #optimize
        lower_bound = x0.min() / MAX_OPTIMIZATION_FACTOR
        upper_bound = x0.max() * MAX_OPTIMIZATION_FACTOR
        positive_bounds = Bounds(lower_bound, upper_bound)

        optimizer_output = minimize(criterion, x0, relative_nutrients_matrix, bounds = positive_bounds)

        mixing_ratio = optimizer_output.x
        score = 1 / optimizer_output.fun

        zeroize_non_significant_factors(mixing_ratio, x0, lower_bound)

    else:
        mixing_ratio = np.zeros_like(x0)
        mixing_ratio[first_better_than_mixed_ind] = 1
        mixing_ratio = x0
        score = 1 / criterion(x0, relative_nutrients_matrix)

    normalized_mixing_ratio = mixing_ratio / mixing_ratio.sum()
    members_keys_list = knowledge_base.get_who_pattern_keys()

    return normalized_mixing_ratio, relative_nutrients_matrix, members_keys_list, score


def zeroize_non_significant_factors(mixing_ratio_out, x0, lower_bound):
    for i in range(len(x0)):
        if x0[i] == 0 or mixing_ratio_out[i] <= lower_bound:
            mixing_ratio_out[i] = 0


def calculate_mixed_profile(x, nutrients_patterns):

    nutrients_patterns_t = nutrients_patterns.transpose()
    result_pattern = np.matmul(nutrients_patterns_t, x)

    return result_pattern


def criterion(x, *args):

    nutrients_patterns = args[0]

    result_pattern = calculate_mixed_profile(x, nutrients_patterns)

    return calculate_score_reciprocal(result_pattern)


def calculate_score_reciprocal(result_pattern):

    return __negative_mean_square_sum(result_pattern)


def is_mixed_better_than_all_single_foods(mixing_ratio, relative_nutrients_matrix):

    is_better = True

    mixed_profile = calculate_mixed_profile(mixing_ratio, relative_nutrients_matrix)
    mixed_score_reciprocal = calculate_score_reciprocal(mixed_profile)

    first_better_than_mixed_ind = 0

    for current_relative_pattern in relative_nutrients_matrix:
        current_score_reciprocal = calculate_score_reciprocal(current_relative_pattern)
        if current_score_reciprocal <= mixed_score_reciprocal:
            is_better = False
            break
        
        first_better_than_mixed_ind += 1

    return is_better, first_better_than_mixed_ind - 1


def __average_deviation(arr):
    ret = (arr / arr.mean()) - 1
    #print("Avg dev: ", str(ret))
    return ret


def __mean_square_sum(arr):
    out_arr = __average_deviation(arr)
    return sum(out_arr**2)


def __negative_mean_square_sum(arr):
    out_arr = __average_deviation(arr)
    ret = sum(out_arr[out_arr < 0]**2)
    #print("Negative mean square sum: ", str(ret))
    return ret



#test code

# def test_optimize_mixing_ratio():

#     food1 = [1.1, 1.2, 0.9, 0.1]
#     food2 = [0.5, 0.4, 0.45, 0.7]
#     food3 = [6.2, 4.3, 6.3, 8.3]
#     # food4 = [4.2, 6.3, 4.3, 4.3]

#     return optimize_mixing_ratio(food1, food2, food3)

# test_arr = np.array([0.8,4,2.1])
# print(mean_square_sum(test_arr))


# print(test_optimize_mixing_ratio())