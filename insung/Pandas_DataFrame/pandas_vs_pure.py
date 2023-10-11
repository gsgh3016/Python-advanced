import random
import timeit
from typing import Dict, Optional
import pandas as pd
import numpy as np
import time

def create_sample_dict() -> Dict[str, Optional[float]]:
    d = {}
    for i in range(50):
        d[f"feature{i}"] = random.random() if random.random() < 0.9 else None
    return d

data_list = [create_sample_dict() for _ in range(1000)]

def null_imputation_using_df():
    df = pd.DataFrame(data_list)
    start = time.time()
    df.fillna(0.0)
    end = time.time()
    print(f"df.fillna(0.0) elapsed:  {(end-start) * 1000:.2f}ms")
    return df

def null_imputation_in_pure_python():
    ret = []
    start = time.time()
    for data in data_list:
        new_data = data.copy()
        for key, val in new_data.items():
            if val is None:
                new_data[key] = 0.0
        ret.append(new_data)
    end = time.time()
    print(f"pure initialize elapsed:  {(end-start) * 1000:.2f}ms")
    return ret

def null_imputation_using_df_np():
    arr = np.array([list(d.values()) for d in data_list], dtype=np.float32)

    df = pd.DataFrame(arr, columns=list(data_list[0].keys()))
    start = time.time()
    df.fillna(0.0)
    end = time.time()
    print(f"df.fillna(0.0) elapsed:  {(end-start) * 1000:.2f}ms")
    return df

elapsed_time = timeit.timeit(null_imputation_using_df, number=1)
print(f"pandas.DataFrame: {elapsed_time * 1000:.2f}ms\n")

elapsed_time = timeit.timeit(null_imputation_in_pure_python, number=1)
print(f"pure python: {elapsed_time * 1000:.2f}ms\n")


elapsed_time = timeit.timeit(null_imputation_using_df_np, number=1)
print(f"pandas.DataFrame: {elapsed_time * 1000:.2f}ms\n")
