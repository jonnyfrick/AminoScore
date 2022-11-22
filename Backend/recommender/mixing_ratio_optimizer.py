
#from recommender import NutrientsPattern
import numpy as np
from scipy.optimize import minimize, Bounds
from recommender import knowledge_base
import random

SIGNIFICANCE_LEVEL = 0.1

def set_initial_values(relative_nutrients_matrix):
    x0 = np.ones(len(relative_nutrients_matrix))
    #x0 = np.random.rand(len(nutrients_lists))
    for i in range(len(x0)):
        over_all_contribution_value = sum(relative_nutrients_matrix[i]) 
        if over_all_contribution_value < SIGNIFICANCE_LEVEL:
            x0[i] = 0
    return x0

def optimize_mixing_ratio(food_nutrients_dicts, age, weight):

    #if accept who recommended summation
    nutrients_lists = knowledge_base.calculate_who_patterns(food_nutrients_dicts)


    nutrients_matrix = np.array(nutrients_lists)
    print(nutrients_matrix)

    relative_nutrients_matrix = knowledge_base.calculate_normalized_intake(nutrients_matrix, age, weight)
    print(relative_nutrients_matrix)

    x0 = set_initial_values(nutrients_lists)
    print("x0: ", str(x0))

    positive_bounds = Bounds(0, 10)
    opmizer_output = minimize(criterion, x0, relative_nutrients_matrix, bounds = positive_bounds)

    mixing_ratio = opmizer_output.x
    normalized_mixing_ratio = mixing_ratio / mixing_ratio.sum()

    #print("Nit: " + str(opmizer_output.nit))
    print("Mixed profile: ", str(calculate_mixed_profile(normalized_mixing_ratio, relative_nutrients_matrix)))
    print(opmizer_output)

    members_keys_list = knowledge_base.get_who_pattern_keys()
    return normalized_mixing_ratio, relative_nutrients_matrix, members_keys_list


def calculate_mixed_profile(x, nutrients_patterns):

    result_pattern = np.zeros_like(nutrients_patterns[0])

    for i in range(len(x)):
        result_pattern += (x[i] * nutrients_patterns[i])

    return result_pattern

def criterion(x, *args):

    nutrients_patterns = args[0]

    result_pattern = calculate_mixed_profile(x, nutrients_patterns)

    return negative_mean_square_sum(result_pattern)


def average_deviation(arr):
    ret = (arr / arr.mean()) - 1
    #print("Avg dev: ", str(ret))
    return ret

def mean_square_sum(arr):
    out_arr = average_deviation(arr)
    return sum(out_arr**2)

def negative_mean_square_sum(arr):
    out_arr = average_deviation(arr)
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