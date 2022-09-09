
# Install cartoframes

Dependencies:
- Python 3.6+
- libgdal-dev
- libgeos-dev
- libproj-dev

To install cartoframes, run this command in your terminal:

```
pip install markupsafe==2.0.1 cartoframes
```

# Authentication

To use cartoframes, you need to authenticate with GEODB's Server. For this you need your master API key. You can find it in your [GEODB's Server account](https://getgeodb.com/). Create a `.env` file in your project's root directory and add your API key. You also need you username and you domain url. For example:

```
GEODB_MASTER_API_KEY=YOUR_API_KEY
GEODB_USERNAME=YOUR_USERNAME
GEODB_SERVER_URI=YOUR_DOMAIN_URL
```

We will first create a `Credentials` object with your API key and then use it to authenticate with GEODB's Server, you need to import the `set_default_credentials` function from `cartoframes.auth` and pass your credentials object. We will also load the dotenv module to load the environment variables from the `.env` file:


```python

import os
from dotenv import load_dotenv
from cartoframes.auth import set_default_credentials
from cartoframes import Credentials

load_dotenv()

auth_credentials = Credentials(
    api_key=os.getenv('GEODB_MASTER_API_KEY'),
    username=os.getenv('GEODB_USERNAME'),
    base_url=os.getenv('GEODB_SERVER_URI')
)

set_default_credentials(auth_credentials)
```


# Creating a dataset

We will create a pandas dataframe and then upload it to GEODB's Server. We will use the `to_carto` function from `cartoframes.io` to upload the dataframe to GEODB's Server. We will also import the `read_csv` function from `pandas` to read the csv file:

```python
from cartoframes.io import to_carto
from geopandas import read_file
gdf = read_file('https://libs.cartocdn.com/cartoframes/samples/starbucks_brooklyn_geocoded.geojson')
gdf = gdf.drop(['cartodb_id'], axis=1)
to_carto(gdf,
         'starbucks_brooklyn_filtered',
         credentials=auth_credentials,
         if_exists='replace')
```

# Querying a dataset
```python
from cartoframes.io import read_carto
gdf = read_carto('SELECT * FROM starbucks_brooklyn_filtered')
gdf.head()
```

# Visualizing a dataset
```python
from cartoframes.viz import Map, Layer
Map(Layer(gdf, 'color: red'))
```

# Appending data to a dataset
```python
from cartoframes.io import append_to_carto
gdf = read_file('https://libs.cartocdn.com/cartoframes/samples/starbucks_queens_geocoded.geojson')
gdf = gdf.drop(['cartodb_id'], axis=1)
append_to_carto(gdf,
                'starbucks_brooklyn_filtered',
                credentials=auth_credentials)
```
