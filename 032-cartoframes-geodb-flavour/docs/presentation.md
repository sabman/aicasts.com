# Using `cartoframes` with GeoDB instances

![](https://content.evernote.com/shard/s542/sh/1553e6b8-c07c-d1b1-6047-080f8232ab4a/f087eb26335d30ded69c4d117d33477c/res/f8ca5bb5-f65c-7171-b4d3-d0d8d1caf9a4)

---

# Authentication

To use `cartoframes`, you need to authenticate with your GeoDB instance. For this you need the following information:

- Your master API key.
- Your username.
- Your GeoDB server instance's URL.


---

## Find your API key

![inline](https://www.evernote.com/l/Ah7rFR1EfKpGU4e2vsmUxBrQFRNQgr-zbT8B/image.png)


---

## Find your username and server url

![inline](https://www.evernote.com/l/Ah6pVc5w3-NHzIX-4IaijpF3Q_YoQKypTYAB/image.png)



---

## Create a `.env` file

Create a `.env` file in your project's root directory and add your API key, username and server url. For example:


```
cat << EOF > .env
GEODB_MASTER_API_KEY=YOUR_API_KEY
GEODB_USERNAME=YOUR_USERNAME
GEODB_SERVER_URI=YOUR_SERVER_URL
EOF
```

---

## Set credentials in your code

```python
import os
from dotenv import load_dotenv
from cartoframes.auth import set_default_credentials
from cartoframes.auth import Credentials
load_dotenv()
GEODB_USERNAME=os.getenv('GEODB_USERNAME')
GEODB_MASTER_API_KEY=os.getenv('GEODB_MASTER_API_KEY')
GEODB_SERVER_URI=os.getenv('GEODB_SERVER_URI')
auth_credentials = Credentials(
    base_url=f"{GEODB_SERVER_URI}/user/{GEODB_USERNAME}", 
    api_key=GEODB_MASTER_API_KEY
)
set_default_credentials(auth_credentials)
```

---

# Creating a dataset

We will create a `geopandas` dataframe from a `geojson` dataset and then upload it to GeoDB:

```python
from cartoframes import to_carto
from geopandas import read_file

gdf = read_file('https://bit.ly/3Dc84I7')
gdf = gdf.drop(['cartodb_id'], axis=1)
to_carto(gdf, 'starbucks_brooklyn')
# Success! Data uploaded to table "starbucks_brooklyn" correctly
# 'starbucks_brooklyn'
```

---

![inline](https://www.evernote.com/l/Ah7gTt8h97FF_o1EUdn2R3JRc-lA9Gr9OIQB/image.png)

---

# Append data to an existing dataset

```python
from cartoframes import to_carto
from geopandas import read_file

gdf = read_file('https://bit.ly/3Dc84I7')
gdf = gdf.drop(['cartodb_id'], axis=1)
# note that we are using the `if_exists` parameter
to_carto(gdf, 'starbucks_brooklyn', if_exists='append')
# Success! Data uploaded to table "starbucks_brooklyn" correctly
# 'starbucks_brooklyn'
```

---

![inline](https://www.evernote.com/l/Ah6S532LrM5Ef4vJ8BWiZLZMNSK1yZLWhjkB/image.png)

---

# Replace data in an existing dataset

```python

from cartoframes import to_carto
from geopandas import read_file

gdf = read_file('https://bit.ly/3Dc84I7')
gdf = gdf.drop(['cartodb_id'], axis=1)
# note that we are using `if_exists='replace'`
to_carto(gdf, 'starbucks_brooklyn', if_exists='replace')
# Success! Data uploaded to table "starbucks_brooklyn" correctly
# 'starbucks_brooklyn'
```

---

# Delete a dataset

```python
from cartoframes import delete_table

delete_table('starbucks_brooklyn')
# Success! Table "starbucks_brooklyn" removed correctly
```
