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

