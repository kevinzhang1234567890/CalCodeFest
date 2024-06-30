#!/usr/bin/env python
# coding: utf-8

# In[4]:


from flask import Flask, request, jsonify, render_template
from model.nlp_model import get_company_score, suggest_alternatives
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_score', methods=['POST'])
def get_score():
    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")
        company_name = str(data.get('Company', ''))
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400

        score = str(get_company_score(company_name))
        alternatives = str(suggest_alternatives(company_name))
        app.logger.error(f"return: company {company_name} score {score}")
        return jsonify({'company': company_name, 'score': score, 'alternatives': alternatives})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




