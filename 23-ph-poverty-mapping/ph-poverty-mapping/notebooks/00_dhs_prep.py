#!/usr/bin/env python
# coding: utf-8

# # Demographic and Health Survey (DHS) Data Preparation
# 
# Download the Philippine National DHS Dataset from the [official website here](https://www.dhsprogram.com/what-we-do/survey/survey-display-510.cfm). Copy and unzip the file in the data directory. Importantly, the DHS folder should contain the following files:
# - `PHHR70DT/PHHR70FL.DTA`
# - `PHHR70DT/PHHR70FL.DO`

# ## Imports

# In[15]:


import pandas as pd


# ## File locations

# In[16]:


data_dir = '../data/'
dhs_zip = data_dir + ''
dhs_file = dhs_zip + 'PHHR71DT/PHHR71FL.DTA'
dhs_dict_file = dhs_zip + 'PHHR71DT/PHHR71FL.DO'
print(dhs_dict_file)


# In[17]:


get_ipython().system('ls ../data/PHHR71DT/PHHR71FL.DO')


# ## Helper Function

# In[18]:


def get_dhs_dict(dhs_dict_file):
    dhs_dict = dict()
    with open(dhs_dict_file, 'r', errors='replace') as file:
        line = file.readline()
        while line:
            line = file.readline()
            if 'label variable' in line:
                code = line.split()[2]
                colname = ' '.join([x.strip('"') for x in line.split()[3:]])
                dhs_dict[code] = colname
    return dhs_dict


# ## Load DHS Dataset

# In[19]:


dhs = pd.read_stata(dhs_file, convert_categoricals=False)
dhs_dict = get_dhs_dict(dhs_dict_file)
dhs = dhs.rename(columns=dhs_dict).dropna(axis=1)
print('Data Dimensions: {}'.format(dhs.shape))


# ## Aggregate Columns

# In[20]:


data = dhs[[
    'Cluster number',
    'Wealth index factor score combined (5 decimals)',
    'Education completed in single years',
    'Has electricity'
]].groupby('Cluster number').mean()

data['Time to get to water source (minutes)'] = dhs[[
    'Cluster number',
    'Time to get to water source (minutes)'
]].replace(996, 0).groupby('Cluster number').median()

data.columns = [[
    'Wealth Index',
    'Education completed (years)',
    'Access to electricity',
    'Access to water (minutes)'
]]

print('Data Dimensions: {}'.format(data.shape))
data.head(10)


# ## Save Processed DHS File

# In[21]:


data.to_csv(data_dir+'dhs_indicators.csv')

