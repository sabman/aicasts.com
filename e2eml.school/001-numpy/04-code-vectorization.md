# Code Vectorizatioon

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
0.10006508103106171
```





```python
import random
from timeit import timeit
# Z1 = random.sample(range(1000), 100)
# Z2 = random.sample(range(1000), 100)

timeit("add_numpy(Z1,Z2)", number = 10000, globals = globals())
```

```
0.2262292149825953
```


