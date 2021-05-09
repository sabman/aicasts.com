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



```py
V = Z[::2,::2]
```

Note some functions return `view` while other return a `copy`.

```python
Z = np.zeros((5,5))
# view
Z.ravel().base is Z
```

```
True
```




```python
# copy
Z.flatten().base is Z
```

```
False
```



This won't scale for big arrays:


```python
X = np.ones(10, dtype=np.int)
Y = np.ones(10, dtype=np.int)
A = 2*X + 2*Y
```



If we don't need to keep the Y and X around then this is better as an in-place solution:

```python
np.multiply(X, 2, out=X)
np.multiply(Y, 2, out=Y)
np.add(X, Y, out=X)
```

```
array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
```



An Exercise: Is `Z2` a view of `Z1`?


```python
Z1 = np.arange(10)
Z2 = Z1[1:-1:2]
print(Z2.base is Z1)
```

```
True
```



To know the actual steps is the questions. So to figure that out we look at the bytes required to move from one element to the next in one dimension. i.e. **strides**.


```python
step = Z2.strides[0] // Z1.strides[0]
print(step)
```

```
2
```



Finding start and stop indicies. For this we can use the `byte_bounds` method that returns a point to the end points of an array.


```python
offset_start = np.byte_bounds(Z2)[0] - np.byte_bounds(Z1)[0]
print(offset_start) # bytes
```

```
8
```




```python
offset_stop = np.byte_bounds(Z2)[-1] - np.byte_bounds(Z1)[-1]
print(offset_stop) # bytes
```

```
-16
```



Converting the offset into indicies: we use `itemsize`


```python
start = offset_start // Z1.itemsize
print(start)
```

```
1
```




```python
stop = Z1.size + offset_stop // Z1.itemsize
print(start, stop, step)
```

```
1 8 2
```


