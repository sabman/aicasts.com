# What is STAC?

STAC is a specification for storing geospatial metadata in a way that is easy to search. It is designed to be flexible and to be able to represent a wide range of geospatial data. It is a community driven project, and welcomes contributions from anyone.

# What problem does STAC solve?

STAC solves the problem of finding geospatial data. It does this by providing a common way to organize and label geospatial data. This allows users to search for data using a common interface. It also allows users to easily find data that is similar to data they already have.

# What's a simple example of using STAC in python?

The following code snippet shows how to use STAC in python to search for data. It uses the [pystac]() library to search for data.

```python
import pystac

# Search for data
search = pystac.Client.open('https://earth-search.aws.element84.com/v0').search(collections=['sentinel-s2-l2a-cogs'], bbox=[-122.6, 37.7, -122.4, 37.8], datetime='2020-01-01/2020-01-02')

# Print the number of items found
print(len(search.get_items()))

# Print the first item found
print(search.get_items()[0])

# Print the first item's geometry
print(search.get_items()[0].geometry)

# Print the first item's datetime
print(search.get_items()[0].datetime)

# Print the first item's properties
print(search.get_items()[0].properties)

# Print the first item's assets
print(search.get_items()[0].assets)

# Print the first item's asset's href
print(search.get_items()[0].assets['B02'].href)

# Print the first item's asset's media type
print(search.get_items()[0].assets['B02'].media_type)

# Print the first item's asset's title
print(search.get_items()[0].assets['B02'].title)

# Print the first item's asset's description
print(search.get_items()[0].assets['B02'].description)

# Print the first item's asset's roles
print(search.get_items()[0].assets['B02'].roles)

# Print the first item's asset's eo:bands
print(search.get_items()[0].assets['B02'].extra_fields['eo:bands'])

# Print the first item's asset's eo:bands' common_name
print(search.get_items()[0].assets['B02'].extra_fields['eo:bands'][0]['common_name'])

# Print the first item's asset's eo:bands' center_wavelength
print(search.get_items()[0].assets['B02'].extra_fields['eo:bands'][0]['center_wavelength'])

# Print the first item's asset's eo:bands' full_width_half_max
print(search.get_items()[0].assets['B02'].extra_fields['eo:bands'][0]['full_width_half_max'])

# Print the first item's asset's eo:bands' description
print(search.get_items()[0].assets['B02'].extra_fields['eo:bands'][0]['description'])

# Print the first item's asset's eo:bands' gsd
print(search.get_items()[0].assets['B02'].extra_fields['eo:bands'][0]['gsd'])

# Print the first item's asset's eo:bands' center_wavelength
print(search.get_items()[0].assets['B02'].extra_fields['eo:bands'][0]['center_wavelength'])

# Download the first item's asset's data
search.get_items()[0].assets['B02'].download('B02.tif')
```

# What's a simple example of using STAC in javascript?

The following code snippet shows how to use STAC in javascript to search for data. It uses the [stac.js]() library to search for data.

```javascript
import { Client } from 'stac.js';

// Search for data
const search = await Client.open('https://earth-search.aws.element84.com/v0').search({collections: ['sentinel-s2-l2a-cogs'], bbox: [-122.6, 37.7, -122.4, 37.8], datetime: '2020-01-01/2020-01-02'});
const items = await search.get_items();

// Print the number of items found
console.log(items.length);
```

# What's a simple example of using STAC in Rust?

The following code snippet shows how to use STAC in Rust to search for data. It uses the [stac]() library to search for data.

```rust
use stac::Client;

// Search for data
let search = Client::open("https://earth-search.aws.element84.com/v0").search(&["sentinel-s2-l2a-cogs"], &[-122.6, 37.7, -122.4, 37.8], "2020-01-01/2020-01-02").await?;

// Print the number of items found
println!("{}", search.get_items().await?.len());
```
