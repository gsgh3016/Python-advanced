import multiprocessing
import time

from fastapi import FastAPI
app = FastAPI()
# uvicorn spawn_overhead:app --reload 

def fibonacci(n: int) -> int:
  return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)

@app.get("/multiprocess") # http://localhost:8000/multiprocess
async def multiprocess_run() -> float:
    start_time = time.time()
    with multiprocessing.Pool(4) as pool:
        pool.map(fibonacci, [25, 25, 25, 25])
    elapsed_time = time.time() - start_time
    print(f"multiprocess elapsed time: {elapsed_time * 1000:.1f}ms")
    return elapsed_time

@app.get("/singleprocess") # http://localhost:8000/singleprocess
async def singleprocess_run() -> float:
    start_time = time.time()
    for _ in range(4):
        fibonacci(25)
    elapsed_time = time.time() - start_time
    print(f"singleprocess elapsed time: {elapsed_time * 1000:.1f}ms")
    return elapsed_time

async def startup_event_handler():
    app.state.process_pool = multiprocessing.Pool(4)

app.add_event_handler("startup", startup_event_handler)

@app.get("/multiprocess_pool")
async def multiprocess_pool_run() -> float:
    start_time = time.time()

    app.state.process_pool.map(fibonacci, [25, 25, 25, 25])

    elapsed_time = time.time() - start_time
    print(f"multiprocess pool elapsed time: {elapsed_time * 1000:.1f}ms")
    return elapsed_time