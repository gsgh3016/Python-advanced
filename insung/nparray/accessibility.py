import timeit
import array
import numpy as np

# Parameters for testing
N = 10000       # number of rows and columns in the array
M = 1000   # number of iterations

# Initialize the arrays
my_list = [i for i in range(N)]
my_array = array.array('i', my_list)
my_ndarray = np.array(my_list)

def test_list_sum():
    sum(my_list)

def test_array_sum():
    sum(my_array)

def test_numpy_sum():
    sum(my_ndarray)

def test_numpy_npsum():
    np.sum(my_ndarray)

# Perform the benchmarks
list_time = timeit.timeit(test_list_sum, number=M)
array_time = timeit.timeit(test_array_sum, number=M)
ndarray_sum_time = timeit.timeit(test_numpy_sum, number=M)
ndarray_npsum_time = timeit.timeit(test_numpy_npsum, number=M)

# Output the results
print(f'list: {list_time * 1000:.1f} ms')
print(f'array: {array_time * 1000:.1f} ms')
print(f'ndarray (sum): {ndarray_sum_time * 1000:.1f} ms')
print(f'ndarray (np.sum): {ndarray_npsum_time * 1000:.1f} ms')