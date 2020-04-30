# PySAL
- [ ] http://darribas.org/gds_scipy16/
- [ ] https://www.tandfonline.com/doi/abs/10.1080/17421772.2019.1593495?journalCode=rsea20
- [ ] https://skymind.ai/wiki/python-ai
- [ ] http://darribas.org/gds_scipy16/ipynb_md/08_spatial_regression.html


http://darribas.org/gds_scipy16/ipynb_md/03_spatial_weights.html


```
import pysal as ps
import pandas as pd
import numpy as np
```

A commonly-used type of weight is a queen contigutiy weight, which reflects adjacency relationships as a binary indicator variable denoting whether or not a polygon shares an edge or a vertex with another polygon. These weights are symmetric, in that when polygon `$A$` neighbors polygon $B$, both` $w{AB} = 1$` and `$w{BA} = 1$`.

```
qW = ps.queen_from_shapefile(shp_path)
dataframe = ps.pdio.read_files(shp_path)
``