#!/usr/bin/env python
# coding: utf-8

# In[3]:


#necessary packages
get_ipython().system('pip install pandas scikit-learn spacy transformers torch tqdm')
get_ipython().system('python3 -m spacy download en_core_web_sm')


# In[3]:


import os
import pandas as pd

def load_data(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                data.append({'filename': filename, 'text': text})
    return pd.DataFrame(data)

# Load data into dataframes
news_data = load_data('data/cleaned/news')
press_releases_data = load_data('data/cleaned/press_releases')
executive_statements_data = load_data('data/cleaned/executive_statements')

#printing the first couple of rows of dataframes
news_data.head(), press_releases_data.head(), executive_statements_data.head()


# In[7]:


import spacy
from spacy.matcher import PhraseMatcher
import pandas as pd

# Loading the spaCy model
nlp = spacy.load('en_core_web_sm')

# List of known technology companies (includes the 15 I used in the queries)
tech_companies = [
    "Apple", "Microsoft", "Google", "Amazon", "Facebook", "Tesla", "Intel",
    "Cisco", "NVIDIA", "IBM", "Qualcomm", "Oracle", "Texas Instruments",
    "Adobe", "Salesforce", "SAP", "Sony", "Samsung", "LG", "HP", "Dell",
    "ASML", "Broadcom", "Micron", "Xiaomi", "Huawei", "AMD", "ARM Holdings",
    "TSMC", "Nokia", "Ericsson", "Lenovo", "Western Digital", "Seagate",
    "Microchip Technology", "Analog Devices", "Marvell Technology"
]

# Creating a PhraseMatcher instance
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Converting company names to spaCy documents
patterns = [nlp.make_doc(company) for company in tech_companies]
matcher.add("TECH_COMPANIES", patterns)

def identify_companies(text):
    doc = nlp(text)
    matches = matcher(doc)
    companies = [doc[start:end].text for match_id, start, end in matches]
    return companies

# Applying the function to each dataset so that only instances of technology companies lsited are recorded
news_data['companies'] = news_data['text'].apply(identify_companies)
press_releases_data['companies'] = press_releases_data['text'].apply(identify_companies)
executive_statements_data['companies'] = executive_statements_data['text'].apply(identify_companies)

# Display the first 50 rows of each dataframe
print(news_data.head(50))
print(press_releases_data.head(50))
print(executive_statements_data.head(50))


# In[8]:


from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tqdm import tqdm

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def encode_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

#using cosine similarity in this function
def compare_claims_bert(claims, impacts):
    claim_embeddings = np.array([encode_text(claim) for claim in tqdm(claims, desc="Encoding Claims")])
    impact_embeddings = np.array([encode_text(impact) for impact in tqdm(impacts, desc="Encoding Impacts")])
    claim_embeddings = claim_embeddings.reshape(len(claims), -1)  # Ensure embeddings are 2D
    impact_embeddings = impact_embeddings.reshape(len(impacts), -1)  # Ensure embeddings are 2D
    similarities = cosine_similarity(claim_embeddings, impact_embeddings)
    return similarities

#press releases such as reports and executive statements are claims that companies make while their real environmental efforts are seen through their actual impact on the environment
claims = press_releases_data['text'].tolist() + executive_statements_data['text'].tolist()
impacts = news_data['text'].tolist()

#finds the similarity in the text between what companies claim to do for the environment in their reports and public statements versus what they actuallly do recorded in news articles
similarities = compare_claims_bert(claims, impacts)
similarities


# In[9]:


def quantify_similarity(similarities):
    return (similarities.mean() * 100).astype(int)

# Quantifies similarity between claims and impact for each company
company_similarity = {}
for company in set(news_data['companies'].explode().dropna()):
    company_news = news_data[news_data['companies'].apply(lambda x: company in x)]
    company_claims = press_releases_data[press_releases_data['companies'].apply(lambda x: company in x)]
    company_claims = pd.concat([company_claims, executive_statements_data[executive_statements_data['companies'].apply(lambda x: company in x)]])

    if not company_news.empty and not company_claims.empty:
        news_claims = company_news['text'].tolist()
        claims = company_claims['text'].tolist()
        similarities = compare_claims_bert(claims, news_claims)
        company_similarity[company] = quantify_similarity(similarities)

# creates dataframe of results
company_similarity_df = pd.DataFrame(list(company_similarity.items()), columns=['Company', 'Similarity'])
print(company_similarity_df)


# In[11]:


#Saves the company similarity scores to a CSV file 
output_df = pd.DataFrame(similarities)
output_df.to_csv('data/output/claim_verification_results_bert.csv', index=False)
company_similarity_df.to_csv('data/output/company_similarity_results_bert.csv', index=False)


# In[ ]:




