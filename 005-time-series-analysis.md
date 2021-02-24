
## TimescaleDB
- [ ] https://blog.timescale.com/blog/sql-functions-for-time-series-analysis/
- [ ] https://blog.hasura.io/using-timescaledb-with-hasura-graphql-d05f030c4b10/
- [ ] https://www.timescale.com/learn/
- [ ] https://tsfresh.readthedocs.io/en/latest/

## General Ideas

- [ ] https://www.kaggle.com/iamleonie/intro-to-time-series-forecasting

```py

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sns # Visualization
import matplotlib.pyplot as plt # Visualization

from sklearn.metrics import mean_absolute_error, mean_squared_error
import math

import warnings # Supress warnings 
warnings.filterwarnings('ignore')
```

```py
df = pd.read_csv("../input/acea-water-prediction/Aquifer_Petrignano.csv")

### Simplifications for the sake of the tutorial ###
# Drop data before 2009 for the purpose of this tutorial
df = df[df.Rainfall_Bastia_Umbra.notna()].reset_index(drop=True)
# Drop one of the target columns, so we can focus on only one target
df = df.drop(['Depth_to_Groundwater_P24', 'Temperature_Petrignano'], axis=1)

# Simplify column names
df.columns = ['Date', 'Rainfall', 'Depth_to_Groundwater', 'Temperature', 'Drainage_Volume', 'River_Hydrometry']

targets = ['Depth_to_Groundwater']
features = [feature for feature in df.columns if feature not in targets]
df.head()
```

