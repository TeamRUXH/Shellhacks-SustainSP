from flask import Flask, request, jsonify
from src import trends

app = Flask(__name__)

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
    pass


@app.route('/get_trends', methods=['POST'])
def getTrends():
    body = request.get_json()
    company_tickers = list(map(lambda x: x.lstrip(), body['company_tickers'].split(',')))
    # print(company_tickers)
    result = trends.getTrends(company_tickers)
    return jsonify(result)
    # return jsonify(company_tickers)

