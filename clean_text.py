#!/usr/bin/env python
# coding: utf-8

# In[12]:


import os
import re
import nltk
from nltk.corpus import stopwords

# Ensuring that the stopwords are available
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Converting text to lowercase
    text = text.lower()
    # Removing HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def clean_text_files(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            #cleaned_text = clean_text(text)
            cleaned_text = text
            #initally created this function to clean the data but realized it would be more effective if I left the data the way it is for BERT to analyze, hence there is no change between processed and cleaned data
            output_file_path = os.path.join(output_dir, f"cleaned_{filename}")
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

# Creating directories for cleaned data (which is really just the processed data)
os.makedirs('data/cleaned/news', exist_ok=True)
os.makedirs('data/cleaned/press_releases', exist_ok=True)
os.makedirs('data/cleaned/executive_statements', exist_ok=True)

# Clean the processed data (does not do anything)
#created this initially but realized it would be best to not implement data cleansing
clean_text_files('data/processed/news', 'data/cleaned/news')
clean_text_files('data/processed/press_releases', 'data/cleaned/press_releases')
clean_text_files('data/processed/executive_statements', 'data/cleaned/executive_statements')


# In[ ]:




