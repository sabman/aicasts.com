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

What are the strides of an array (bytes to step in each dimension):


```python
# strides = Z.shape[1]*Z.itemsize, Z.itemsize
# print(strides)
print(Z.strides)
strides = Z.strides
```

```
(4,)
```




```python
offset_start = 0
index = 1,1
for i in range(Z.ndim):
    offset_start += strides[i]*index[i]

offset_end = offset_start + Z.itemsize
```




```python
Z = np.arange(9).reshape(3,3).astype(np.int16)
index = 1,1
print(Z[index].tobytes())

offset = 0
for i in range(Z.ndim):
    offset += Z.strides[i]*index[i]
print(Z.tobytes()[offset_start:offset_end])
```

```
b'\x04\x00'
b'\x02\x00\x03\x00'
```


