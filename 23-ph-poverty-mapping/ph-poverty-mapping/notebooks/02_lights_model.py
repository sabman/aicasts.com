#!/usr/bin/env python
# coding: utf-8

# # Nightlight Summary Statistics Model

# ## Imports

# In[1]:


import os
import sys
sys.path.insert(0, '../utils')
import model_utils
import data_utils

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[9]:


# !pip install google-cloud-storage
get_ipython().system('source ../.env')


# In[18]:


import dotenv
dotenv.load_dotenv("../.env", override=True)
from google.cloud import storage
storage_client = storage.Client()


# ## File Locations

# In[22]:


# Google Cloud Storage
bucket_name = 'tm-geospatial'
directory = 'poverty-prediction-datasets'

# Destination paths
ntl_summary_stats_file = '../data/nightlights_summary_stats.csv'
dhs_indicators_file = '../data/dhs_indicators.csv'


# ## Download Datasets

# In[20]:


# Download from Google Cloud Storage
data_utils.download_from_bucket('nightlights_summary_stats.csv', directory, ntl_summary_stats_file, bucket_name);
data_utils.download_from_bucket('dhs_indicators.csv', directory, dhs_indicators_file, bucket_name);


# In[21]:


get_ipython().system('wget https://raw.githubusercontent.com/thinkingmachines/ph-poverty-mapping/master/data/nightlights_summary_stats.csv')


# ## Load Datasets

# In[23]:


# Load nighttime lights dataset
ntl_summary_stats = pd.read_csv(ntl_summary_stats_file, encoding="ISO-8859-1")
dhs_indicators = pd.read_csv(dhs_indicators_file)
dhs = ntl_summary_stats.merge(dhs_indicators, left_on='DHSCLUST', right_on='Cluster number')

# Define feature columns
feature_cols = ['cov', 'kurtosis', 'max', 'mean', 'median', 'min', 'skewness', 'std']


# ## Correlations

# In[24]:


data_utils.plot_corr(
    data=dhs,
    features_cols=feature_cols,
    indicator = 'Wealth Index',
    figsize=(5,3)
)


# ## Machine Learning Pipeline

# ### Configuration

# In[28]:


# Scoring metrics
scoring = {
    'r2': data_utils.pearsonr2,
    'rmse': data_utils.rmse
}

# Indicators of interest
indicators = [
    'Wealth Index',
    'Education completed (years)',
    'Access to electricity',
    'Access to water (minutes)'
]


# ### Random Forest

# In[29]:


predictions = model_utils.evaluate_model(
    data=dhs,
    feature_cols=feature_cols, 
    indicator_cols=indicators, 
    scoring=scoring,
    model_type='random_forest', 
    refit='r2', 
    search_type='random', 
    n_splits=5, 
    n_iter=10
)


# ### XGBoost

# In[27]:


predictions = model_utils.evaluate_model(
    data=dhs,
    feature_cols=feature_cols, 
    indicator_cols=indicators, 
    scoring=scoring,
    model_type='xgboost', 
    refit='r2', 
    search_type='random', 
    n_splits=5, 
    n_iter=10
)


# ### Lasso Regression

# In[8]:


predictions = model_utils.evaluate_model(
    data=dhs,
    feature_cols=feature_cols, 
    indicator_cols=indicators, 
    scoring=scoring,
    model_type='lasso', 
    refit='r2', 
    search_type='grid', 
    n_splits=5
)


# ### Ridge Regression

# In[9]:


predictions = model_utils.evaluate_model(
    data=dhs,
    feature_cols=feature_cols, 
    indicator_cols=indicators, 
    scoring=scoring,
    model_type='ridge', 
    refit='r2', 
    search_type='grid', 
    n_splits=5
)

