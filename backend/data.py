import yfinance as yf
import pandas as pd
import numpy as np
import pydash

import cache

def getCompanyNameFromTicker(ticker):
    company = yf.Ticker(ticker)
    company_name = company.info['longName']
    return company_name

# TODO Get a better source for S&P Companies. These change relatively infrequently
# so it may be fine for now
def getSPCompanies():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500_list = np.array(sp500[0]['Symbol'])
    return sp500_list

def getCompanyNameFromTickers(tickers = []):
    cached_data = cache.get_cache('getCompanyNameFromTickers')
    if cached_data: return cached_data

    if not len(tickers): return []
    tickerData = yf.Tickers(' '.join(tickers))
    formatted_tickers = map(lambda ticker: { 'ticker': ticker, 'name': pydash.get(tickerData, 'tickers.{}.info.longName'.format(ticker))}, tickers)

    data = list(formatted_tickers)
    cache.put_cache('getCompanyNameFromTickers', data)
    return data

if __name__ == '__main__':
    tickers = getSPCompanies()
    data = getCompanyNameFromTickers(tickers)
    print(data)