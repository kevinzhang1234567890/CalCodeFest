#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import matplotlib.pyplot as plt

# Loads dataframe from the CSV file
company_scores = pd.read_csv('data/output/company_similarity_results_bert.csv')

# Sorts the dataframe by the 'Similarity' column in descending order
company_scores = company_scores.sort_values(by='Similarity', ascending=False)

# Plotting the bar chart directly from the sorted dataframe
plt.figure(figsize=(14, 8))  # increases figure size for better readability
plt.bar(company_scores['Company'], company_scores['Similarity'], color='skyblue')
plt.xlabel('Company')
plt.ylabel('Similarity')
plt.title('Similarity Distribution of Different Companies')
plt.xticks(rotation=90, ha='right')  # Rotating labels to 90 degrees and aligning them to the right
plt.ylim(0, 100)  

# Adding the similarity value on top of each bar
for index, value in enumerate(company_scores['Similarity']):
    plt.text(index, value + 1, str(value), ha='center')

plt.tight_layout()  # Adjusting layout to ensure everything fits without overlap
plt.show()


# In[ ]:




