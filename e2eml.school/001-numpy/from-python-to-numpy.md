source: https://www.labri.fr/perso/nrougier/from-python-to-numpy/#id1


```py

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

```

```py
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
```
