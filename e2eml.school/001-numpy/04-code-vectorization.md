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
0.11206055301590823
```





```python
import random
from timeit import timeit
Z1 = random.sample(range(1000), 100)
Z2 = random.sample(range(1000), 100)

timeit("add_numpy(Z1,Z2)", number = 10000, globals = globals())
```

```
0.24996316598844714
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


Temporal vectorization

The interesting (and slow) part of this code is the mandelbrot function that actually computes the sequence fc(fc(fc...))). The vectorization of such code is not totally straightforward because the internal return implies a differential processing of the element. Once it has diverged, we don't need to iterate any more and we can safely return the iteration count at divergence. The problem is to then do the same in numpy. But how?



```python
def mandelbrot_numpy_2(xmin, xmax, ymin, ymax, xn, yn, itermax, horizon=2.0):
    Xi, Yi = np.mgrid[0:xn, 0:yn]
    Xi, Yi = Xi.astype(np.uint32), Yi.astype(np.uint32)
    X = np.linspace(xmin, xmax, xn, dtype=np.float32)[Xi]
    Y = np.linspace(ymin, ymax, yn, dtype=np.float32)[Yi]
    C = X + Y*1j
    N_ = np.zeros(C.shape, dtype=np.uint32)
    Z_ = np.zeros(C.shape, dtype=np.complex64)
    Xi.shape = Yi.shape = C.shape = xn*yn

    Z = np.zeros(C.shape, np.complex64)
    for i in range(itermax):
        if not len(Z): break

        # Compute for relevant points only
        np.multiply(Z, Z, Z)
        np.add(Z, C, Z)

        # Failed convergence
        I = abs(Z) > horizon
        N_[Xi[I], Yi[I]] = i+1
        Z_[Xi[I], Yi[I]] = Z[I]

        # Keep going with those who have not diverged yet
        np.negative(I,I)
        Z = Z[I]
        Xi, Yi = Xi[I], Yi[I]
        C = C[I]
    return Z_.T, N_.T
```



We now want to measure the fractal dimension of the Mandelbrot set using the Minkowski–Bouligand dimension. To do that, we need to do box-counting with a decreasing box size (see figure below). As you can imagine, we cannot use pure Python because it would be way too slow. The goal of the exercise is to write a function using numpy that takes a two-dimensional float array and returns the dimension. We'll consider values in the array to be normalized (i.e. all values are between 0 and 1).

## Spatial vectorization

Spatial vectorization refers to a situation where elements share the same computation but are in interaction with only a subgroup of other elements. This was already the case for the game of life example, but in some situations there is an added difficulty because the subgroup is dynamic and needs to be updated at each iteration. This the case, for example, in particle systems where particles interact mostly with local neighbours. This is also the case for "boids" that simulate flocking behaviors.


```python
import math
import random
from vec2 import vec2

class Boid:
    def __init__(self, x=0, y=0):
        self.position = vec2(x, y)
        angle = random.uniform(0, 2*math.pi)
        self.velocity = vec2(math.cos(angle), math.sin(angle))
        self.acceleration = vec2(0, 0)
```

```
---------------------------------------------------------------------------ModuleNotFoundError
Traceback (most recent call last)<ipython-input-1-24da46298b2b> in
<module>
      1 import math
      2 import random
----> 3 from vec2 import vec2
      4
      5 class Boid:
ModuleNotFoundError: No module named 'vec2'
```




```python
def separation(self, boids):
    count = 0
    for other in boids:
        d = (self.position - other.position).length()
        if 0 < d < desired_separation:
            count += 1
            ...
    if count > 0:
        ...

 def alignment(self, boids): ...
 def cohesion(self, boids): ...
```

```
  File "<tokenize>", line 11
    def alignment(self, boids): ...
    ^
IndentationError: unindent does not match any outer indentation level
```




```python
class Flock:
    def __init__(self, count=150):
        self.boids = []
        for i in range(count):
            boid = Boid()
            self.boids.append(boid)

    def run(self):
        for boid in self.boids:
            boid.run(self.boids)
```



numpy implementation takes a different approach and we'll gather all our boids into a position array and a velocity array


```python
n = 500
velocity = np.zeros((n, 2), dtype=np.float32)
position = np.zeros((n, 2), dtype=np.float32)

dx = np.subtract.outer(position[:, 0], position[:, 0])
dy = np.subtract.outer(position[:, 1], position[:, 1])
distance = np.hypot(dx, dy)
```



https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
https://numpy.org/doc/stable/reference/generated/numpy.hypot.html


```python
mask_0 = (distance > 0)
mask_1 = (distance < 25)
mask_2 = (distance < 50)
mask_1 *= mask_0
mask_2 *= mask_0
mask_3 = mask_2
```




```python
mask_1_count = np.maximum(mask_1.sum(axis=1), 1)
mask_2_count = np.maximum(mask_2.sum(axis=1), 1)
mask_3_count = mask_2_count
```


