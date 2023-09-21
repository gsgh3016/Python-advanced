import timeit
import array
import numpy as np
import pickle
import marshal
import random

N = 10000     # number of elements in the array
M = 1000      # number of iterations

# Initialize the arrays
my_list = [random.random() for _ in range(N)]
my_list_enc = marshal.dumps(my_list)

my_array = array.array('f', my_list)
my_array_enc = marshal.dumps(my_array)

my_ndarray = np.array(my_list, dtype=np.float32)
my_ndarray_enc = marshal.dumps(my_ndarray)

def test_list_marshal():
    marshal.dumps(my_list)

def test_list_unmarshal():
    marshal.loads(my_list_enc)

def test_array_marshal():
    marshal.dumps(my_array)

def test_array_unmarshal():
    marshal.loads(my_array_enc)

def test_ndarray_marshal():
    marshal.dumps(my_ndarray)

def test_ndarray_unmarshal():
    marshal.loads(my_ndarray_enc)

# Perform the benchmarks
list_marshal_time = timeit.timeit(test_list_marshal, number=M)
array_marshal_time = timeit.timeit(test_array_marshal, number=M)
ndarray_marshal_time = timeit.timeit(test_ndarray_marshal, number=M)

list_unmarshal_time = timeit.timeit(test_list_unmarshal, number=M)
array_unmarshal_time = timeit.timeit(test_array_unmarshal, number=M)
ndarray_unmarshal_time = timeit.timeit(test_ndarray_unmarshal, number=M)

print("[marshal]")
print(f'list: {list_marshal_time * 1000:.1f} ms')
print(f'array: {array_marshal_time * 1000:.1f} ms')
print(f'ndarray: {ndarray_marshal_time * 1000:.1f} ms')

print()
print("[unmarshal]")
print(f'list: {list_unmarshal_time * 1000:.1f} ms')
print(f'array: {array_unmarshal_time * 1000:.1f} ms')
print(f'ndarray: {ndarray_marshal_time * 1000:.1f} ms')
