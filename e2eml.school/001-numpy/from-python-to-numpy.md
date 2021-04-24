source: https://www.labri.fr/perso/nrougier/from-python-to-numpy/#id1

Numpy is all about vectorization. If you are familiar with Python, this is the main difficulty you'll face because you'll need to change your way of thinking and your new friends (among others) are named "vectors", "arrays", "views" or "ufuncs".

Let's take a very simple example, random walk. One possible object oriented approach would be to define a RandomWalker class and write a walk method that would return the current position after each (random) step. It's nice, it's readable, but it is slow:


### Object oriented approach



```python
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import random
```




```python
class RandomWalker:
    def __init__(self):
        self.position = 0

    def walk(self, n):
        self.position = 0
        for i in range(n):
            yield self.position
            self.position += 2*random.randint(0, 1) - 1

walker = RandomWalker()
walk = [position for position in walker.walk(1000)]
# print(walk[0:10])
```



Benchmarking gives us:


```python
import timeit
walker = RandomWalker()
# timeit.timeit("[position for position in walker.walk(n=10000)]", number=10000)
# 10 loops, best of 3: 15.7 msec per loop
```



### Procedural approach

For such a simple problem, we can probably save the class definition and concentrate only on the walk method that computes successive positions after each random step.

```py

def random_walk(n):
    position = 0
    walk = [position]
    for i in range(n):
        position += 2*random.randint(0, 1)-1
        walk.append(position)
    return walk

walk = random_walk(1000)
print(walk[0:10])

```

### Vectorized approach


```python
def random_walk_faster(n=1000):
    from itertools import accumulate
    # only available from python 3.6

    steps = random.choices([-1, +1], k=n)
    return [0]+list(accumulate(steps))

walk = random_walk_faster(n=10000)
print(walk[0:10])

from timeit import timeit
timeit("random_walk_faster(n=10000)", number=10000, globals = globals())
```

```
[0, 1, 2, 1, 2, 3, 2, 3, 4, 3]
```

```
40.632896060997155
```


