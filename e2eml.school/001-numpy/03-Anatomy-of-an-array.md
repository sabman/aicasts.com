# Anatomy of an array


```python
import numpy as np
Z = np.ones(4*1000000, np.float32)
# Z[...] = 0
Z.view(np.int8)[...] = 0
```




## Memory layout

```py
Z = np.arrange(9).reshape(3,3).astype(np.int16)
print(Z)

print(Z.itemsize)
print(Z.shape)
print(Z.ndim)
```
