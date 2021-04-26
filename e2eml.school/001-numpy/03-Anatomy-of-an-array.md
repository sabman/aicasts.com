# Anatomy of an array

Fastest way to reset an array...

```python
import numpy as np
Z = np.ones(4*1000000, np.float32)
# Z[...] = 0
Z.view(np.int8)[...] = 0
```


