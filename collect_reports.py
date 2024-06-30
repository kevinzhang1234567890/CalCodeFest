#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import os
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key from environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Create directories for raw data
os.makedirs('data/raw/press_releases', exist_ok=True)

def fetch_news(query, page=1):
    url = f'https://newsapi.org/v2/everything?q={query}&page={page}&pageSize=50&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch news: {response.status_code}, Page: {page}")
        return None

def save_news_articles(articles, filename):
    with open(f'data/raw/press_releases/{filename}', 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

#15 tech companies expected to see high growth
queries = [
    "NVIDIA environment report",
    "TSMC environment report",
    "AMD environment report",
    "Tesla environment report",
    "Qualcomm environment report",
    "Micron environment report",
    "Intel environment report",
    "Apple environment report",
    "Amazon environment report",
    "Samsung environment report",
    "Microsoft environment report",
    "Huawei environment report",
    "Cisco environment report",
    "ASML environment report",
    "Sony environment report"
]

all_articles = []

# Fetch and save news reports for each query
for query in queries:
    page = 1
    news_data = fetch_news(query, page)
    if news_data and 'articles' in news_data:
        all_articles.extend(news_data['articles'])
        print(f"Fetched {len(news_data['articles'])} articles for query: '{query}'")
        time.sleep(1)  # Adding delay to avoid hitting rate limits
    else:
        print(f"No articles fetched or an error occurred for query: '{query}'")

if all_articles:
    save_news_articles(all_articles, 'tech_sustainability_reports.json')
    print(f"Total articles fetched: {len(all_articles)}")
else:
    print("No articles fetched or an error occurred")


# In[ ]:




