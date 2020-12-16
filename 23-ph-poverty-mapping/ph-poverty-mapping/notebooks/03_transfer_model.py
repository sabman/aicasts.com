#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[1]:


import os
import sys
sys.path.insert(0, '../utils')
import transfer_utils 
import model_utils
import data_utils

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tqdm import tqdm
import numpy as np
import pandas as pd

import torchsummary
import torchvision
import torch
from transfer_model import NTLModel

import warnings
import logging
warnings.filterwarnings("ignore")
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

import wandb
wandb.init(project="tm-poverty-prediction")

use_gpu = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device(use_gpu)
print("Using gpu: ", use_gpu)

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[10]:


get_ipython().system('pip install wandb torch torchvision torchsummary xgboost')
 


# ## File Locations

# In[ ]:


# see: https://github.com/thinkingmachines/ph-poverty-mapping/issues/7#issuecomment-494645573

# Google Cloud Storage
bucket_name = 'tm-geospatial'
dir = 'poverty-prediction-datasets'
image_dir = dir + '/images'

# Destination files
# data_dir = '../data/zoom17/'
data_dir = '../data/'
report_file = data_dir+'report/report.csv'
nightlights_unstacked_file = data_dir+'nightlights_unstacked.csv'

dhs_indicators_file = data_dir+'dhs_indicators.csv'
dhs_provinces_file = data_dir+'dhs_provinces.csv'
dhs_regions_file = data_dir+'dhs_regions.csv'

gsm_data_dir = data_dir+'images/' 
model_file = '../models/model_best.pt'
feature_embeddings_file = data_dir+'embeddingsv2.csv'
embeddings_indicators_file = data_dir+'indicators.csv'

# Test images for sanity checking purposes
high1_file = data_dir+'test_images/high1.jpg'
high2_file = data_dir+'test_images/high2.jpg'
low1_file = data_dir+'test_images/low1.jpg'
low2_file = data_dir+'test_images/low2.jpg'


# ## Load Datasets

# In[7]:


report = pd.read_csv(report_file)
nightlights_unstacked = pd.read_csv(nightlights_unstacked_file)
dhs_indicators = pd.read_csv(dhs_indicators_file)
dhs_regions = pd.read_csv(dhs_regions_file)
dhs_provinces = pd.read_csv(dhs_provinces_file)


# ## Instantiate Transfer Model

# In[4]:


# Load data
dataloaders, dataset_sizes, class_names = transfer_utils.load_transform_data(
    data_dir=gsm_data_dir, batch_size=4
)

# Instantiate model
model = torchvision.models.vgg16(pretrained=True)
model = NTLModel(model, len(class_names))
if use_gpu == "cuda":
    model = model.cuda()
    
# Load saved model
checkpoint = torch.load(model_file)
model.load_state_dict(checkpoint['state_dict'])

# Visualize model
torchsummary.summary(model, (3, 400, 400))


# ## Visualize Nighttime Light Intensity Classification Predictions

# In[6]:


transfer_utils.visualize_model(model, dataloaders, class_names, 5, size=(5,5));


# In[7]:


# Get feature embeddings for selected test images
high1_embedding = transfer_utils.get_embedding(high1_file, model, gpu=True)
high2_embedding = transfer_utils.get_embedding(high2_file, model, gpu=True)
low1_embedding = transfer_utils.get_embedding(low1_file, model, gpu=True)
low2_embedding = transfer_utils.get_embedding(low2_file, model, gpu=True)

# Display test images
figsize = (5,5)
plt.figure(figsize=figsize)
plt.imshow(mpimg.imread(high1_file))
plt.show()
plt.figure(figsize=figsize)
plt.imshow(mpimg.imread(high2_file))
plt.show()
plt.figure(figsize=figsize)
plt.imshow(mpimg.imread(low1_file))
plt.show()
plt.figure(figsize=figsize)
plt.imshow(mpimg.imread(low2_file))
plt.show()

# Sanity check: Get cosine similarity between feature embeddings
cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
print("Embedding size: {}".format(high1_embedding.size()))
print('Cosine similarity between 2 high nightlight intensity images: {0}'.format(cos(high1_embedding,high2_embedding)))
print('Cosine similarity between 2 low nightlight intensity images: {0}'.format(cos(low1_embedding,low2_embedding)))
print('Cosine similarity between 1 low and 1 high: {0}'.format(cos(low1_embedding,high2_embedding)))
print('Cosine similarity 1 high and 1 low: {0}'.format(cos(high1_embedding,low2_embedding)))


# ## Generate feature embedding per cluster

# In[ ]:


# Get feature embedding per image
report.filename = report.filename.str.replace('../../data/gsm_data/images/', '../data/images/')
report = nightlights_unstacked.merge(report, left_on='ID', right_on='id', how='left')
report = transfer_utils.get_embedding_per_image(report, model)
print("Report shape: {}".format(report.shape))

# Sanity check: Get feature embedding for 1 high light intensity image and 1 low intensity image
high = torch.from_numpy(np.array([report[report['label'] == 'high'].iloc[0]['embeddings']]))
low = torch.from_numpy(np.array([report[report['label'] == 'low'].iloc[5]['embeddings']]))

# Sanity Check: Cosine similarity between pairs of images
cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
print("Cosine similarity is: {}".format(cos(low, high)))


# In[9]:


# Get mean feature embedding per cluster
cluster_embeddings = transfer_utils.get_mean_embedding_per_cluster(report)

# Merge cluster embeddings with DHS indicators
cluster_embeddings = cluster_embeddings.merge(dhs_indicators, left_on='cluster', right_on='Cluster number')
feature_embeddings = cluster_embeddings.mean_embedding.apply(pd.Series)

# Save embeddings 
feature_embeddings.to_csv(feature_embeddings_file)
cluster_embeddings.to_csv(embeddings_indicators_file)


# ## Machine Learning Pipeline

# In[4]:


scoring = {
    'r2': data_utils.pearsonr2,
    'rmse': data_utils.rmse
}

indicators = [
    'Wealth Index',
    'Education completed (years)',
    'Access to electricity',
    'Access to water (minutes)'
]


# In[21]:


# Load embedding features
embeddings_df = pd.read_csv(feature_embeddings_file).iloc[:, 1:]
cluster_embeddings = pd.read_csv(embeddings_indicators_file)

region_cols = list(dhs_regions.columns[:-1])
province_cols = list(dhs_provinces.columns[:-1])
embedding_cols = list(embeddings_df.columns) 

# Merge with DHS indicators
embeddings_df['Cluster number'] = cluster_embeddings['Cluster number']
data = embeddings_df.merge(cluster_embeddings, on='Cluster number')

# Merge with regional and provincial indicators
data = data.merge(dhs_regions, on='Cluster number', how='left')
data = data.fillna(0)

print(data.shape)


# ## t-SNE Visualization

# In[28]:


embeddings = data.iloc[:, :4096]
feature_cols = embeddings.columns

embeddings['Cluster number'] = data['Cluster number']
embeddings['Wealth Index'] = data['Wealth Index']

# Sanity check embeddings
data.iloc[:, [-24, 0, 1, 2]].tail(3)


# In[29]:


from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(embeddings[feature_cols].values)


# In[30]:


embeddings['x-tsne'] = tsne_results[:,0]
embeddings['y-tsne'] = tsne_results[:,1]

f, ax = plt.subplots()
points = ax.scatter(embeddings['x-tsne'], embeddings['y-tsne'], c=embeddings['Wealth Index'], cmap='Blues', alpha=0.5)
f.colorbar(points);


# ## Machine Learning Pipeline

# ### Using CNN feature embeddings + Regional indicators

# In[31]:


predictions = model_utils.evaluate_model(
    data=data,
    feature_cols=embedding_cols+region_cols, 
    indicator_cols=indicators, 
    wandb=wandb,
    scoring=scoring,
    model_type='ridge', 
    refit='r2', 
    search_type='grid', 
    n_splits=5 ,
    n_workers=1
)


# ### Using CNN feature embeddings 

# In[33]:


predictions = model_utils.evaluate_model(
    data=data,
    wandb=None,
    feature_cols=embedding_cols, 
    indicator_cols=indicators, 
    scoring=scoring,
    model_type='ridge', 
    refit='r2', 
    search_type='grid', 
    n_splits=5,
    n_workers=1
)

