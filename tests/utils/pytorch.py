import torch
import time
import numpy as np

num_params = 10
s = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_s.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (4*((s * (1 - s)))).sum()
start_time_pytorch = time.time()
y.backward()
s.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
s_list = s.grad.tolist()

for i in range(num_params):
	print(str(s_list[i]))
