import torch
import numpy as np

x = torch.from_numpy(np.array([1., 1., 1., 1.]))
x.requires_grad = True 
y = torch.from_numpy(np.array([1., 1., 1., 1.]))
y.requires_grad = True  
z = torch.from_numpy(np.array([1., 1., 1., 1.]))
z.requires_grad = True  

a = (torch.sin(x) * torch.cos(y) + z).sum()

print(a)

a.backward()

print(x.grad, " ", y.grad)