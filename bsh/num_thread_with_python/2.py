import os
import time
import multiprocessing as mp
import torch

def foo(i: int) -> None:
    matrix_a = torch.rand(size=(1000, 1000))
    matrix_b = torch.rand(size=(1000, 1000))
    # warm up
    for _ in range(10):
        torch.matmul(matrix_a, matrix_b)

    start_time = time.perf_counter()
    for _ in range(100):
        torch.matmul(matrix_a, matrix_b)
    print(i, time.perf_counter() - start_time)

if __name__ == "__main__":
	# 특정 pid를 가지는 프로세스를 실행할 수 있는 cpu코어의 개수
    num_processes = len(os.sched_getaffinity(0))
    print("num_processes: ", num_processes)
    with mp.Pool(num_processes) as pool:
        pool.map(foo, range(num_processes))