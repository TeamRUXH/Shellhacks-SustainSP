from flask import Flask, request, jsonify
from src import trends

app = Flask(__name__)

@app.route('/', methods=['POST'])
def getTrends():
    body = request.get_json()
    company_tickers = list(map(lambda x: x.lstrip(), body['company_tickers'].split(',')))
    # print(company_tickers)
    result = trends.getTrends(company_tickers)
    return jsonify(result)
    # return jsonify(company_tickers)