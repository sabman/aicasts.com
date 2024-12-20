# Theory

# Libraries

- xdggs: discrete global grid systems with xarray https://www.youtube.com/watch?v=bAMGFKsxsjs&list=PPSV


Pangeo Showcase talk on Dec 4, 2024 by Justis Magin. Discrete Global Grid Systems (DGGS) are innovative spatial reference systems that provide a systematic spatial subdivision of spherical or ellipsoidal objects. Unlike traditional latitude and longitude grids or unstructured meshes, the object’s surface is recursively subdivided into equally sized and uniquely identifiable cells, forming a tree or hierarchy of cells. This allows assigning a numeric ID to each cell, which can be used for efficient traversal of the hierarchy for operations like up-/downsampling, neighbours search, and alignment / co-location.

xdggs is a library that extends xarray to work with data on a DGGS by leveraging the information contained in the numeric cell IDs. It supports tasks like selecting and visualizing data, as well as computing geographic coordinates for cell centers and boundaries, allowing the integration with “traditional” GIS data systems and libraries.

https://xdggs.readthedocs.io/en/latest/