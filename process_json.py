#!/usr/bin/env python
# coding: utf-8

# In[21]:


import os
import json

# Create directories for processed data
os.makedirs('data/processed/news', exist_ok=True)
os.makedirs('data/processed/press_releases', exist_ok=True)
os.makedirs('data/processed/executive_statements', exist_ok=True)

def extract_text_from_json(input_file, output_dir):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for i, article in enumerate(data):
        text = 'Title: ' + str(article.get('title','')) + '\nDescription: ' + str(article.get('description', '')) + '\nContent: ' + str(article.get('content', ''))
        #formatting data to display article title, description, and content in standardized manner
        output_file_path = os.path.join(output_dir, f'article_{i+1}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)

# Processing the collected data
extract_text_from_json('data/raw/news/tech_environmental_impact.json', 'data/processed/news')
extract_text_from_json('data/raw/press_releases/tech_sustainability_reports.json', 'data/processed/press_releases')
extract_text_from_json('data/raw/executive_statements/executive_statements.json', 'data/processed/executive_statements')


# In[ ]:




