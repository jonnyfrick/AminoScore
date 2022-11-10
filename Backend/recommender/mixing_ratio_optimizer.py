
#from recommender import NutrientsPattern
import numpy as np
from scipy.optimize import minimize, Bounds
import random

def optimize_mixing_ratio(nutrients_lists):

    x0 = np.ones(len(nutrients_lists))
    foods = np.array(nutrients_lists)

    positive_bounds = Bounds(0, 10)
    opmizer_output = minimize(criterion, x0, foods, bounds = positive_bounds)
    mixing_ratio = opmizer_output.x
    print(mixing_ratio.mean())
    normalized_mixing_ratio = mixing_ratio / mixing_ratio.sum()

    print("Nit: " + str(opmizer_output.nit))

    return normalized_mixing_ratio
     

def criterion(x, *args):

    nutrients_patterns = args[0]

    result_pattern = np.zeros_like(nutrients_patterns[0])

    for i in range(len(x)):
        result_pattern += x[i] * nutrients_patterns[i]

    return negative_mean_square_sum(result_pattern)


def average_deviation(arr):
    return (arr / arr.mean()) - 1

def mean_square_sum(arr):
    out_arr = average_deviation(arr)
    return sum(out_arr**2)

def negative_mean_square_sum(arr):
    out_arr = average_deviation(arr)
    return sum(out_arr[out_arr < 0]**2)


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