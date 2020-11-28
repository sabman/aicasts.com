#!/usr/bin/env python
# coding: utf-8

# # Demographic and Health Survey (DHS) Data Preparation
# 
# Download the Philippine National DHS Dataset from the [official website here](https://www.dhsprogram.com/what-we-do/survey/survey-display-510.cfm). Copy and unzip the file in the data directory. Importantly, the DHS folder should contain the following files:
# - `PHHR70DT/PHHR70FL.DTA`
# - `PHHR70DT/PHHR70FL.DO`

# ## Imports

# In[49]:


import pandas as pd


# ## File locations

# In[50]:


data_dir = '../data/'
dhs_zip = data_dir + '<INSERT DHS FOLDER NAME HERE>/'
dhs_file = dhs_zip + 'PHHR70DT/PHHR70FL.DTA'
dhs_dict_file = dhs_zip + 'PHHR70DT/PHHR70FL.DO'


# ## Helper Function

# In[51]:


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

# In[55]:


dhs = pd.read_stata(dhs_file, convert_categoricals=False)
dhs_dict = get_dhs_dict(dhs_dict_file)
dhs = dhs.rename(columns=dhs_dict).dropna(axis=1)
print('Data Dimensions: {}'.format(dhs.shape))


# ## Aggregate Columns

# In[56]:


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
data.head(2)


# ## Save Processed DHS File

# In[54]:


data.to_csv(data_dir+'dhs_indicators.csv')

