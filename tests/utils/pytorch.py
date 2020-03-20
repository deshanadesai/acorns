import torch
import time
import numpy as np

num_params = 30010
K = torch.tensor(np.load('./tests/utils/numpy_params/function_1_param_K.npy'), requires_grad=True, dtype=torch.float)
L = torch.tensor(np.load('./tests/utils/numpy_params/function_1_param_L.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = (4*4*((K * (1 - K))*(L * (1 - L)))).sum()
start_time_pytorch = time.time()
y.backward()
K.grad
L.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
K_list = K.grad.tolist()
L_list = L.grad.tolist()

for i in range(num_params):
	print(str(K_list[i]))
	print(str(L_list[i]))
