import torch
import time
import numpy as np

num_params = 10
T = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_T.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (4*((T * (1 - T)))).sum()
start_time_pytorch = time.time()
y.backward()
T.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
T_list = T.grad.tolist()

for i in range(num_params):
	print(str(T_list[i]))
