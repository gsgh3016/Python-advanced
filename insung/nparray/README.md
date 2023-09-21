## #2 Built-in list는 충분히 빠르지 않다. 필요시 array나 numpy를 사용하자.

##### 파이썬 built-in list 구현
```
/* Python built-in list */
typedef struct {
    PyObject_VAR_HEAD
    /* Vector of pointers to list elements.  list[0] is ob_item[0], etc. */
    PyObject **ob_item;

    Py_ssize_t allocated;
} PyListObject;
```
##### 파이썬 built-in array 구현
```
/* Python built-in array */
typedef struct arrayobject {
    PyObject_VAR_HEAD
    char *ob_item;
    Py_ssize_t allocated;
    const struct arraydescr *ob_descr;
    PyObject *weakreflist; /* List of weak references */
    Py_ssize_t ob_exports;  /* Number of exported buffers */
} arrayobject;
```
##### Numpy nparray 구현
```
numpy/numpy/core/src/multiarray
/arrayobject.c
/* NumPy nparray */
static PyObject *
array_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"shape", "dtype", "buffer", "offset", "strides",
                             "order", NULL};
    PyArray_Descr *descr = NULL;
    int itemsize;
    PyArray_Dims dims = {NULL, 0};
    PyArray_Dims strides = {NULL, -1};
    PyArray_Chunk buffer;
    npy_longlong offset = 0;
    NPY_ORDER order = NPY_CORDER;
    int is_f_order = 0;
    PyArrayObject *ret;

    buffer.ptr = NULL;
    ...
}
``` 

##### 파이썬 built-in sum 구현
```
cpython/Python/bltinmodule.c
/* Python built-in-sum */
static PyObject *
builtin_sum_impl(PyObject *module, PyObject *iterable, PyObject *start)
/*[clinic end generated code: output=df758cec7d1d302f input=162b50765250d222]*/
{
    PyObject *result = start;
    PyObject *temp, *item, *iter;

    iter = PyObject_GetIter(iterable);
    if (iter == NULL)
        return NULL;

    if (result == NULL) {
        result = PyLong_FromLong(0);
        if (result == NULL) {
            Py_DECREF(iter);
            return NULL;
        }
    } else {
        /* reject string values for 'start' parameter */
        if (PyUnicode_Check(result)) {
            PyErr_SetString(PyExc_TypeError,
                "sum() can't sum strings [use ''.join(seq) instead]");
            Py_DECREF(iter);
            return NULL;
        }
        if (PyBytes_Check(result)) {
            PyErr_SetString(PyExc_TypeError,
                "sum() can't sum bytes [use b''.join(seq) instead]");
            Py_DECREF(iter);
            return NULL;
        }
        if (PyByteArray_Check(result)) {
            PyErr_SetString(PyExc_TypeError,
                "sum() can't sum bytearray [use b''.join(seq) instead]");
            Py_DECREF(iter);
            return NULL;
        }
        Py_INCREF(result);
    }
```

##### Numpy sum 구현 (Wrapper)
```
numpy/numpy/core/fromnumeric.py
/* Numpy-sum (Wrapper)*/
@array_function_dispatch(_sum_dispatcher)
def sum(a, axis=None, dtype=None, out=None, keepdims=np._NoValue,
        initial=np._NoValue, where=np._NoValue):
 if isinstance(a, _gentype):
        # 2018-02-25, 1.15.0
        warnings.warn(
            "Calling np.sum(generator) is deprecated, and in the future will give a different result. "
            "Use np.sum(np.fromiter(generator)) or the python sum builtin instead.",
            DeprecationWarning, stacklevel=2)

        res = _sum_(a)
        if out is not None:
            out[...] = res
            return out
        return res

    return _wrapreduction(a, np.add, 'sum', axis, dtype, out, keepdims=keepdims,
                          initial=initial, where=where)
```

##### Numpy sum 동작 방식
```
numpy/numpy/core/src/umath/reduction.c
/* Numpy-sum */
NPY_NO_EXPORT PyArrayObject *
PyUFunc_ReduceWrapper(PyArrayMethod_Context *context,
        PyArrayObject *operand, PyArrayObject *out, PyArrayObject *wheremask,
        npy_bool *axis_flags, int keepdims,
        PyObject *initial, PyArray_ReduceLoopFunc *loop,
        npy_intp buffersize, const char *funcname, int errormask)
{
    assert(loop != NULL);
    PyArrayObject *result = NULL;
    npy_intp skip_first_count = 0;

    /* Iterator parameters */
    NpyIter *iter = NULL;
    PyArrayObject *op[3];
    PyArray_Descr *op_dtypes[3];
    npy_uint32 it_flags, op_flags[3];
    /* Loop auxdata (must be freed on error) */
    NpyAuxData *auxdata = NULL;
    ...
}
```


### list, array, numpy ndarray의 접근 성능 비교
/* accessibility.py */
```
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
```
실행 결과
```
list: 49.6 ms
array: 152.1 ms
ndarray (sum): 465.4 ms
ndarray (np.sum): 7.2 ms
```

### list, array, numpy ndarray의 직렬화 성능 비교
/* serialization.py */
```import timeit
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
```
실행 결과
```
[marshal]
list: 120.6 ms
array: 11.7 ms
ndarray: 1.2 ms

[unmarshal]
list: 219.2 ms
array: 1.1 ms
ndarray: 1.2 ms
```
