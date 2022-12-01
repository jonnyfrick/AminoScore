import numba
from jax import jit
#from numba import jit
from numba.typed import List
import numpy as np
import time

@jit
def list_test(input):

    out_list = List()

    for i in range(len(input)):
        for j in range(len(input)):
            out_list.append(i * j)

    return out_list


@jit
def jit_loop_single_instruction_array_test(input):
    N = len(input)
    out_array = np.ones((N,N), dtype=float)

    iterations = 0
    for i in range(len(input)):
        for j in range(len(input)):
            out_array[i][j] = i * j
            iterations += 1

    return iterations

def loop_single_instruction_array_test(input):

    N = len(input)
    out_array = np.zeros((N,N), dtype=float)

    iterations = 0
    for i in range(len(input)):
        for j in range(len(input)):
            out_array[i][j] = i * j
            iterations += 1

    return iterations

@jit
def jit_array_mult_test(input):

    tic = time.time()
    
    N = len(input)
    array_1 = np.ones((N,N), dtype=float)
    array_2 = np.ones((N,N), dtype=float)

    result_array = array_1 * array_2
    toc = time.time()
    return toc - tic



def array_mult_test(input):

    tic = time.time()
    
    N = len(input)
    array_1 = np.ones((N,N), dtype=float)
    array_2 = np.ones((N,N), dtype=float)

    result_array = array_1 * array_2
    toc = time.time()
    return toc - tic



def performance_test(no_jit_func, jit_func, list):


    no_jit_time = no_jit_func(list)


    print("no jit: ", str(no_jit_time))


    jit_time = jit_func(list)

    print("jit: ", str(jit_time))

    print("speedup: ", str(no_jit_time / jit_time))







#numba_list = List(list(range(10000)))
numba_list = list(range(10000))

#performance_test(loop_single_instruction_array_test, jit_loop_single_instruction_array_test, numba_list)

performance_test(array_mult_test, jit_array_mult_test, numba_list)