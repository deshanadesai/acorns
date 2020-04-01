import torch
import time
import numpy as np

num_params = 10
a = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_a.npy'), requires_grad=True, dtype=torch.float)
b = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_b.npy'), requires_grad=True, dtype=torch.float)
c = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_c.npy'), requires_grad=True, dtype=torch.float)
d = torch.tensor(np.load('./tests/utils/numpy_params/function_0_param_d.npy'), requires_grad=True, dtype=torch.float)
torch.set_num_threads(1)
y = ((a*a+b*b+c*c+d*d)*(1+1/((a*d-b*c)*(a*d-b*c)))).sum()
start_time_pytorch = time.time()
y.backward()
a.grad
b.grad
c.grad
d.grad

end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print(str(runtime))
a_list = a.grad.tolist()
b_list = b.grad.tolist()
c_list = c.grad.tolist()
d_list = d.grad.tolist()

for i in range(num_params):
	print(str(a_list[i]))
	print(str(b_list[i]))
	print(str(c_list[i]))
	print(str(d_list[i]))
