import torch
import time
import numpy as np

k = torch.tensor(np.load('utils/params.npy'), requires_grad=True)
torch.set_num_threads(1)
y = ((k*k+3*k)-k/4)/k+k*k*k*k+k*k*(22/7*k)+k*k*k*k*k*k*k*k*k
start_time_pytorch = time.time()
y.backward(torch.ones_like(k))
k.grad
end_time_pytorch = time.time()
runtime = (end_time_pytorch - start_time_pytorch)
print( str(runtime) + " " + " ".join(str(x) for x in k.grad.tolist()))
