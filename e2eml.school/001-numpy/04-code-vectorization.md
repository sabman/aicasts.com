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
0.10625019199505914
```





```python
import random
from timeit import timeit
Z1 = random.sample(range(1000), 100)
Z2 = random.sample(range(1000), 100)

timeit("add_numpy(Z1,Z2)", number = 10000, globals = globals())
```

```
0.35445997200440615
```



## Uniform vectorization

Simplest form of vectorization. Where all elements share the same computation at every iteration of processing the vector. Game of Life is a good example.

> The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead. Every cell interacts with its eight neighbours, which are the cells that are directly horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

> - Any live cell with fewer than two live neighbours dies, as if by needs caused by underpopulation.
> - Any live cell with more than three live neighbours dies, as if by overcrowding.
> - Any live cell with two or three live neighbours lives, unchanged, to the next generation.
> - Any dead cell with exactly three live neighbours becomes a live cell.

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




```python
def iterate(Z):
    N = compute_neighbours(Z)
    for x in range(1,shape[0]-1):
        for y in range(1,shape[1]-1):
             if Z[x][y] == 1 and (N[x][y] < 2 or N[x][y] > 3):
                 Z[x][y] = 0
             elif Z[x][y] == 0 and N[x][y] == 3:
                 Z[x][y] = 1
    return Z
```




## Numpy implementation



```python
N = np.zeros(Z.shape, dtype=int)
N[1:-1,1:-1] += (Z[ :-2, :-2] + Z[ :-2,1:-1] + Z[ :-2,2:] +
                 Z[1:-1, :-2]                + Z[1:-1,2:] +
                 Z[2:  , :-2] + Z[2:  ,1:-1] + Z[2:  ,2:])
```

```
---------------------------------------------------------------------------AttributeError
Traceback (most recent call last)<ipython-input-1-a66d88b4d01b> in
<module>
----> 1 N = np.zeros(Z.shape, dtype=int)
      2 N[1:-1,1:-1] += (Z[ :-2, :-2] + Z[ :-2,1:-1] + Z[ :-2,2:] +
      3                  Z[1:-1, :-2]                + Z[1:-1,2:] +
      4                  Z[2:  , :-2] + Z[2:  ,1:-1] + Z[2:  ,2:])
AttributeError: 'list' object has no attribute 'shape'
```



Rules enforcement:


```python
# Flatten arrays
N_ = N.ravel()
Z_ = Z.ravel()

# Apply rules
R1 = np.argwhere( (Z_==1) & (N_ < 2) )
R2 = np.argwhere( (Z_==1) & (N_ > 3) )
R3 = np.argwhere( (Z_==1) & ((N_==2) | (N_==3)) )
R4 = np.argwhere( (Z_==0) & (N_==3) )

# Set new values
Z_[R1] = 0
Z_[R2] = 0
Z_[R3] = Z_[R3]
Z_[R4] = 1

# Make sure borders stay null
Z[0,:] = Z[-1,:] = Z[:,0] = Z[:,-1] = 0
```

```
---------------------------------------------------------------------------NameError
Traceback (most recent call last)<ipython-input-1-9b34b1bbcc10> in
<module>
      1 # Flatten arrays
----> 2 N_ = N.ravel()
      3 Z_ = Z.ravel()
      4
      5 # Apply rules
NameError: name 'N' is not defined
```



## Temporal vectorization

The Mandelbrot set:


```python
def mandelbrot_python(xmin, xmax, ymin, ymax, xn, yn, maxiter, horizon=2.0):
    def mandelbrot(z, maxiter):
        c = z
        for n in range(maxiter):
            if abs(z) > horizon:
                return n
            z = z*z + c
        return maxiter
    r1 = [xmin+i*(xmax-xmin)/xn for i in range(xn)]
    r2 = [ymin+i*(ymax-ymin)/yn for i in range(yn)]
    return [mandelbrot(complex(r, i),maxiter) for r in r1 for i in r2]
```


