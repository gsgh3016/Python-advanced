import multiprocessing
import random
import time
from typing import List

from fastapi import FastAPI

async def startup_event_handler():
    app.state.process_pool = multiprocessing.Pool(4)

app = FastAPI()
# uvicorn communicate_overhead:app --reload 

app.add_event_handler("startup", startup_event_handler)

def generate_random_vector(size: int) -> List[float]:
    return [random.random() for _ in range(size)]

def element_wise_sum(vectors: List[List[float]]) -> List[float]:
    ret_vector = [0.0] * len(vectors[0])
    for vector in vectors:
        for i in range(len(vector)):
            ret_vector[i] += vector[i]
    return ret_vector

@app.get("/multiprocess") # http://localhost:8000/multiprocess
async def multiprocess() -> List[float]:
    vectors = [generate_random_vector(512) for _ in range(100)]

    start_time = time.time()
    result_vector_list = app.state.process_pool.map(element_wise_sum, [
        vectors[:25], vectors[25:50], vectors[50:75], vectors[75:],
    ])
    ret_vector = element_wise_sum(result_vector_list)

    elapsed_time = time.time() - start_time
    print(f"multiprocess elapsed time: {elapsed_time * 1000:.1f}ms")
    return ret_vector

@app.get("/singleprocess") # http://localhost:8000/singleprocess
async def singleprocess_run() -> List[float]:
    vectors = [generate_random_vector(512) for _ in range(100)]

    start_time = time.time()
    ret_vector = element_wise_sum(vectors)

    elapsed_time = time.time() - start_time
    print(f"singleprocess elapsed time: {elapsed_time * 1000:.1f}ms")
    return ret_vector