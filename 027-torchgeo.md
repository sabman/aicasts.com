# Why TorchGeo? What problem does it solve?

> ... help realize the potential of deep learning for remote sensing applications, we introduce TorchGeo

- What is PyTorch?

PyTorch is a library for training deep learning models.

- What is TorchGeo?

TorchGeo is a library for simplifying the application of deep learning methodology to remotely sensed data by integrating geospatial data into the PyTorch deep learning ecosystem


- What is Remotely sensed geospatial data?

Remotely sensed data refers to data collected about the planet earth, but isn't limited to Earth. It could be other planets, moons, asteroids and even stars. On Earth the data is colleted using sensors that are deployed to platforms. These platforms and sensors both vary a great deal. For example remote sensing data may come from platfroms in space (using satellites) or within the earth's atmosphere (using aircraft or drones) and in the ocean (on the hulls of ships or submersible). As you can see from the above statement these platforms alone range hugely in varity. So do the sensors and thus the data. Sensors can range from those designed to collect data about the atmopsheric gasses to underwater trenchs. There is an incredible variety of data that comes from remote sensing.

The final data products of remote sensing are images. These images vary in their resolution (both spectral and spatial) they have metadata related to their spatial reference system. 

- Why is it important?

> However, the variance in data collection methods and handling of geospatial metadata make the application of deep learning methodology to remotely sensed data nontrivia

Remote sensing has been a crucial technology in the scientific understanding of our plant. It has thus applications in climate science, forestry, precision agriculture, marine science, disaster rsponse

# How do I use TorchGeo in the context of Remote Sensing, ML and AI

```python
# GETTING STARTED
# In this tutorial, we demonstrate some of the basic features of TorchGeo and show how easy it is to use if you’re already familiar with other PyTorch domain libraries like torchvision.

# It’s recommended to run this notebook on Google Colab if you don’t have your own GPU. Click the “Open in Colab” button above to get started.


import os
import tempfile

from torch.utils.data import DataLoader

from torchgeo.datasets import NAIP, ChesapeakeDE, stack_samples
from torchgeo.datasets.utils import download_url
from torchgeo.samplers import RandomGeoSampler

# For this tutorial, we’ll be using imagery from the National Agriculture Imagery Program (NAIP) and labels from the Chesapeake Bay High-Resolution Land Cover Project. First, we manually download a few NAIP tiles and create a PyTorch Dataset.
data_root = tempfile.gettempdir()
naip_root = os.path.join(data_root, "naip")
naip_url = "https://naipblobs.blob.core.windows.net/naip/v002/de/2018/de_060cm_2018/38075/"
tiles = [
    "m_3807511_ne_18_060_20181104.tif",
    "m_3807511_se_18_060_20181104.tif",
    "m_3807512_nw_18_060_20180815.tif",
    "m_3807512_sw_18_060_20180815.tif",
]
for tile in tiles:
    download_url(naip_url + tile, naip_root)

naip = NAIP(naip_root)

chesapeake_root = os.path.join(data_root, "chesapeake")

# Next, we tell TorchGeo to automatically download the corresponding Chesapeake labels.
chesapeake = ChesapeakeDE(chesapeake_root, crs=naip.crs, res=naip.res, download=True)

# Finally, we create an IntersectionDataset so that we can automatically sample from both GeoDatasets simultaneously.
dataset = naip & chesapeake

# Sampler (RandomGeoSampler)
# Unlike typical PyTorch Datasets, TorchGeo GeoDatasets are indexed using lat/long/time bounding boxes. This requires us to use a custom GeoSampler instead of the default sampler/batch_sampler that comes with PyTorch.
sampler = RandomGeoSampler(naip, size=1000, length=10)

# DataLoader
# Now that we have a Dataset and Sampler, we can combine these into a single DataLoader.
dataloader = DataLoader(dataset, sampler=sampler, collate_fn=stack_samples)

# Training
# Other than that, the rest of the training pipeline is the same as it is for torchvision.
for sample in dataloader:
    image = sample["image"]
    target = sample["mask"]
```

# Where does TorchGeo fit in an organisational context?
