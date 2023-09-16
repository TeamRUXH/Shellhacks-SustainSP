import yfinance as yf
import pandas as pd
import time
from pytrends.request import TrendReq
import json

def getCompanyNameFromTicker(ticker):
    company = yf.Ticker(ticker)
    company_name = company.info['longName']
    return company_name

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

# Example usage
if __name__ == '__main__':
    # Let's stress test
    company_tickers = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG",
        "JPM", "BAC", "WFC", "C", "GS"          # Example tickers (Top banks)
        "T", "VZ", "TMUS", "S", "CCI",           # Example tickers (Telecom companies)
    ]
    
    company_list = list(set(list(map(lambda ticker: getCompanyNameFromTicker(ticker), company_tickers))))
    data = getTrends(company_list)
    print(data)
