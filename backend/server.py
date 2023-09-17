from flask import Flask, request, jsonify
import trends

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import data as hdata
import trends
import esg
import volatility
import sentiment

# Routes for the server

''' 
@TODO
Need a route for getting a list of top `pageSize` sustainable companies.
The companies should will initially be scored using a linear function based on a default weighting formula
which can later also be adjusted
'''

@app.route('/everything', methods=['POST'])
def getEverything():
    ''' 
    Let's use a static list of top 500 companies
    Subject the top 500 companies to all the different metrics
    Use the weights to calculate a unified score
    Return the tickers by score
    '''
    # Get company tickers
    company_names = hdata.getCompanyNameFromTickers()
    esg_scores = esg.getESGForCompanies()
    relevance_scores = trends.getRelevanceScore()
    volatility_scores = volatility.getStableStocks()

    formatting = {}
    # Get company names
    for company in company_names:
        formatting[company['ticker']] = {}
        formatting[company['ticker']]['name'] = company['name']

    # Get esgRiskScore
    for score in esg_scores:
        ticker = list(score.keys())[0]
        formatting[ticker]['esgRiskScore'] = 'Not Available' if "Total ESG Risk Score" not in score[ticker] else score[ticker]["Total ESG Risk Score"]

    # Get relevanceScore
    for score in relevance_scores:
        formatting[score]['relevanceScore'] = relevance_scores[score]
    
    # Get volatilityScore
    for ticker in volatility_scores:
        formatting[ticker]['volatilityScore'] = volatility_scores[ticker]['volatility']
        formatting[ticker]['marketCap'] = volatility_scores[ticker]['Market Cap']

    return jsonify(formatting)


@app.route('/company', methods=['POST'])
def getCompany():
    body = request.get_json()
    ticker = body['ticker']

    # Get esg
    data = esg.getESGData(ticker)
    companyName = hdata.getCompanyNameFromTicker(ticker)
    data['sentiment'] = sentiment.performSentimentalAnalysis(companyName)
    result = trends.getTrends([ticker])
    data['trends'] = result[ticker]

    return jsonify(data)

@app.route('/get_trends', methods=['POST'])
def getTrends():
    body = request.get_json()
    company_tickers = list(map(lambda x: x.lstrip(), body['company_tickers'].split(',')))
    # print(company_tickers)
    return jsonify(result)
    # return jsonify(company_tickers)
