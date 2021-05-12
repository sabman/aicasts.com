# Code Vectorization

This means the problem you are trying to solve is inherently vectorizable. In other words you don't need to rethink your problem to solve it with numpy. For an example lets look at suming two lists of integers.

regular python:


```python
def add_python(Z1,Z2):
  return [z1+z2 for (z1,z2) in zip(Z1,Z2)]
```



now numpy:

```python
import numpy as np
def add_numpy(Z1,Z2):
  return np.add(Z1,Z2)
```



let's benchmark:


```python
import random
from timeit import timeit
Z1 = random.sample(range(1000), 100)
Z2 = random.sample(range(1000), 100)

timeit("add_python(Z1,Z2)", number = 10000, globals = globals())
```

```
0.10828315600156202
```





```python
import random
from timeit import timeit
Z1 = random.sample(range(1000), 100)
Z2 = random.sample(range(1000), 100)

timeit("add_numpy(Z1,Z2)", number = 10000, globals = globals())
```

```
0.20328883299953304
```



## Uniform vectorization

Simplist form of vectorization. Where all elements share the same computation at every iteration of processing the vector. Game of Life is a good example.

We can implement the Game of Life rules and steps as follows:


```python
Z = [[0,0,0,0,0,0],
     [0,0,0,1,0,0],
     [0,1,0,1,0,0],
     [0,0,1,1,0,0],
     [0,0,0,0,0,0],
     [0,0,0,0,0,0]]
```




```python
def compute_neighbours(Z):
    shape = len(Z), len(Z[0])
    N  = [[0,]*(shape[0]) for i in range(shape[1])]
    for x in range(1,shape[0]-1):
        for y in range(1,shape[1]-1):
            N[x][y] = Z[x-1][y-1]+Z[x][y-1]+Z[x+1][y-1] \
                    + Z[x-1][y]            +Z[x+1][y]   \
                    + Z[x-1][y+1]+Z[x][y+1]+Z[x+1][y+1]
    return N
```


