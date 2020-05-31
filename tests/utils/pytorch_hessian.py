import torch
import time
import numpy as np
import torch.autograd.functional as F

num_params = 40010
k = torch.tensor(np.load('./tests/utils/numpy_params/function_2_param_k.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)

def make_func(k):
     return (torch.sin(k) +torch. cos(k) +torch. pow(k, 2)).sum()
     
start_time_pytorch = time.time()

output = F.hessian(make_func, k.data)

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))

output = output.data.numpy()
for i in range(num_params):
    print(output[i][i])