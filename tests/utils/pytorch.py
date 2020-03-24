import torch
import time
import numpy as np

num_params = 4010
B = torch.tensor(np.load('./tests/utils/numpy_params/function_2_param_B.npy'), requires_grad=True, dtype=torch.float)
a = torch.tensor(np.load('./tests/utils/numpy_params/function_2_param_a.npy'), requires_grad=True, dtype=torch.float)
W = torch.tensor(np.load('./tests/utils/numpy_params/function_2_param_W.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (4*4*4*((B * (1 - B))*(a * (1 - a))*(W * (1 - W)))).sum()
start_time_pytorch = time.time()
y.backward()
B.grad
a.grad
W.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
B_list = B.grad.tolist()
a_list = a.grad.tolist()
W_list = W.grad.tolist()

for i in range(num_params):
	print(str(B_list[i]))
	print(str(a_list[i]))
	print(str(W_list[i]))
