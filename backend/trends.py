import pandas as pd
import time
from pytrends.request import TrendReq
import json

import data as hdata
import cache

def getTrends(company_list, tf='today 12-m'):
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=3, backoff_factor=1)
    batches = [company_list[i:i + 5] for i in range(0, len(company_list), 5)]
    
    def getDF(batch):
        pytrends.build_payload(batch, cat=0, timeframe=tf, gprop="")
        data = pytrends.interest_over_time()
        df = pd.DataFrame(data)
    
        # Drop isPartial column
        df = df.drop('isPartial', axis=1)

        # Get average for monbth
        monthly_mean = df.resample('M').mean()
        return monthly_mean

    dataframes = map(getDF, batches)
    concatenated_df = pd.concat(dataframes, axis=1)
    concatenated_df.reset_index(drop=True)
    return json.loads(concatenated_df.to_json(orient="columns"))

def getRelevanceScore():
    companies = hdata.getCompanyNameFromTickers()
    cached_data = cache.get_cache('getRelevanceScore')
    if cached_data: return cached_data

    # ticker + name in company in companies
    company_data = {}
    for company in companies:
        try:
            trendsData = getTrends([company['name']])
            for company_name, values in trendsData.items():
                relevance_score = sum(values.values()) / len(values)
            
                # Update the dictionary with the relevance score
                company_data[company['ticker']] = relevance_score
        except:
            company_data[company['ticker']] = 'Not Available'

    cache.put_cache('getRelevanceScore', company_data)
    return company_data


# Example usage
if __name__ == '__main__':
    sol = getRelevanceScore()
    print(sol)
    # Let's stress test
    # company_tickers = [
    #     "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG",
    #     "JPM", "BAC", "WFC", "C", "GS"          # Example tickers (Top banks)
    #     "T", "VZ", "TMUS", "S", "CCI",           # Example tickers (Telecom companies)
    # ]
    
    # company_list = list(set(list(map(lambda ticker: getCompanyNameFromTicker(ticker), company_tickers))))
    # data = getTrends(company_list)
    # print(data)
