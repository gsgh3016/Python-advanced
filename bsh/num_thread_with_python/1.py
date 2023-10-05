import numpy as np
import torch

numpy_a = np.empty(shape=(10000, 10000))
numpy_b = np.empty(shape=(10000, 10000))
numpy_a @ numpy_b

torch_a = torch.from_numpy(numpy_a)
torch_b = torch.from_numpy(numpy_b)
torch_a @ torch_b