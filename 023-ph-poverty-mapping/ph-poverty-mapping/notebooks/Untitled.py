#!/usr/bin/env python
# coding: utf-8

# In[1]:


from numpy.linalg import norm
from numpy import dot
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# In[6]:


a = np.array([1, 0, -1, 6, 8])
b = np.array([0, 11, 4, 7, 6])


# In[12]:


d = np.linalg.norm(a-b)


# In[13]:


d


# In[14]:


# In[15]:


cosine_similarity([a, b])


# In[16]:


np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# In[17]:


cos_sim = dot(a, b)/(norm(a)*norm(b))


# In[18]:


cos_sim


# In[ ]:
