import torch
import time
import numpy as np

num_params = 90010
k = torch.tensor(np.load('utils/numpy_params/function_0_param_k.npy'), requires_grad=True, dtype=torch.float)
j = torch.tensor(np.load('utils/numpy_params/function_0_param_j.npy'), requires_grad=True, dtype=torch.float)
l = torch.tensor(np.load('utils/numpy_params/function_0_param_l.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (torch.sin(k) +torch. cos(j) +torch. pow(l, 2)).sum()
start_time_pytorch = time.time()
y.backward()
k.grad
j.grad
l.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
k_list = k.grad.tolist()
j_list = j.grad.tolist()
l_list = l.grad.tolist()

for i in range(num_params):
	print(str(k_list[i]))
	print(str(j_list[i]))
	print(str(l_list[i]))
