import timeit
from dataclasses import dataclass

ITERATIONS = 100000

class MyClass:
    def __init__(self, key1, key2, key3):
        self.key1 = key1
        self.key2 = key2
        self.key3 = key3

@dataclass
class MyDataclass:
    key1: int
    key2: int
    key3: int

def create_dict():
    my_dict = {"key1": 1, "key2": 2, "key3": 3}

def create_class():
    MyClass(1, 2, 3)

def create_dataclass():
    MyDataclass(1, 2, 3)

dict_time = timeit.timeit(create_dict, number=ITERATIONS)
class_time = timeit.timeit(create_class, number=ITERATIONS)
dataclass_time = timeit.timeit(create_dataclass, number=ITERATIONS)

print(f"dictionary creation time: {dict_time * 1000:.2f} ms")
print(f"class creation time: {class_time * 1000:.2f} ms")
print(f"dataclass creation time: {dataclass_time * 1000:.2f} ms")