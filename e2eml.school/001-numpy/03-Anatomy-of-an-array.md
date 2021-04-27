# Anatomy of an array


```python
import numpy as np
Z = np.ones(4*1000000, np.float32)
# Z[...] = 0
Z.view(np.int8)[...] = 0
```



