#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd

# Load your similarity scores
df = pd.read_csv('company_similarity_results_bert.csv')

def get_company_score(company_name):
    try:
        score = df[df['Company'] == company_name]['Similarity'].values[0]
    except IndexError:
        score = "Company not found"
    return score

def suggest_alternatives(company_name):
    alternatives = df[df['Company'] != company_name].sort_values(by='Similarity', ascending=False).head(3)
    return alternatives['Company'].tolist()


# In[ ]:




