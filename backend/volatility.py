import yfinance as yf
from functools import reduce

import data as hdata
import cache

def getStableStocks(min_market_cap = 1e10, max_volatility = 0.3, period="1y"):
    cached_data = cache.get_cache('getStableStocks')
    if cached_data: return cached_data
    
    tickers = hdata.getSPCompanies()
    data = yf.download(' '.join(tickers), period=period, group_by='ticker')

    # Define your criteria
    # Minimum market capitalization (adjust as needed)
    # Maximum volatility (adjust as needed)

    # Calculate market capitalization and volatility
    market_cap = {}
    volatility = {}

    for ticker in tickers:
        try:
            df = data[ticker]
            last_close = df['Close'][-1]
            shares_outstanding = yf.Ticker(ticker).info['sharesOutstanding']
            mkt_cap = last_close * shares_outstanding
            market_cap[ticker] = mkt_cap

            # Calculate volatility (you can use your own formula)
            daily_returns = df['Adj Close'].pct_change().dropna()
            vol = daily_returns.std()
            volatility[ticker] = vol
        except:
            volatility[ticker] = 'Not Available'

    # Filter companies based on criteria
    filtered_tickers = [ticker for ticker in tickers if (ticker in market_cap and market_cap[ticker] >= min_market_cap) and (ticker in volatility and volatility[ticker] <= max_volatility)]

    # Sort by market capitalization (top 100)
    top_tickers = sorted(filtered_tickers, key=lambda ticker: -market_cap[ticker])

    result = {}   
    for ticker in top_tickers:
        result[ticker] = { "Market Cap": market_cap[ticker], "volatility": volatility[ticker]}
    
    cache.put_cache('getStableStocks', result)
    return result

if __name__ == "__main__":    
    # Fetch historical data for a list of tickers over the past year
    data = getStableStocks()
    print(data)
    