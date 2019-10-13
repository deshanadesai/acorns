import torch
import time
import numpy as np

<<<<<<< HEAD
num_params = 2010
k = torch.tensor(np.load('utils/numpy_params/function_0_param_k.npy'), requires_grad=True, dtype=torch.float)
j = torch.tensor(np.load('utils/numpy_params/function_0_param_j.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k*j).sum()
=======
num_params = 90010
k = torch.tensor(np.load('utils/numpy_params/function_0_param_k.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k).sum()
>>>>>>> c837a98c0f019023ef5fe45295646abd7160e6c9
start_time_pytorch = time.time()
y.backward()
k.grad
j.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
k_list = k.grad.tolist()
j_list = j.grad.tolist()

for i in range(num_params):
	print(str(k_list[i]))
	print(str(j_list[i]))
