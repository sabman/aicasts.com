#!/usr/bin/env python
# coding: utf-8

# In[1]:


import seaborn as sns
sns.set_theme(style="whitegrid")
tips = sns.load_dataset("tips")
ax = sns.stripplot(x=tips["total_bill"])


# In[70]:


sns.__version__


# In[16]:


import pandas as pd


# In[46]:


tips[tips.day == "Sun"]


# In[57]:


rec = tips.iloc[[77,90,19,1]]


# In[58]:





# In[59]:


type(tips)


# In[60]:


# recdf = pd.DataFrame(rec).transpose()
# recdf


# In[69]:


ax = sns.stripplot(x="day", y="total_bill", data=tips, jitter=0.05, size=3)
sns.stripplot(x="day", y="total_bill", data=rec, marker="o", ax=ax, size=6)


# In[62]:


ax.figure


# In[23]:


ax = sns.violinplot(x="day", y="total_bill", data=tips,
                    inner=None, color=".8")
ax = sns.stripplot(x="day", y="total_bill", data=tips)


# In[ ]:




