import yfinance as yf
from functools import reduce

def getStableStocks(tickers, min_market_cap = 1e10, max_volatility = 0.3, period="1y"):
    data = yf.download(tickers, period=period, group_by='ticker')

    # Define your criteria
    # Minimum market capitalization (adjust as needed)
    # Maximum volatility (adjust as needed)

    # Calculate market capitalization and volatility
    market_cap = {}
    volatility = {}

    for ticker in tickers:
        df = data[ticker]
        last_close = df['Close'][-1]
        shares_outstanding = yf.Ticker(ticker).info['sharesOutstanding']
        mkt_cap = last_close * shares_outstanding
        market_cap[ticker] = mkt_cap

        # Calculate volatility (you can use your own formula)
        daily_returns = df['Adj Close'].pct_change().dropna()
        vol = daily_returns.std()
        volatility[ticker] = vol

    # Filter companies based on criteria
    filtered_tickers = [ticker for ticker in tickers if market_cap[ticker] >= min_market_cap and volatility[ticker] <= max_volatility]

    # Sort by market capitalization (top 100)
    top_100_tickers = sorted(filtered_tickers, key=lambda ticker: -market_cap[ticker])[:100]

    result = {}   
    for ticker in top_100_tickers:
        result[ticker] = { "Market Cap": market_cap[ticker], "volatility": volatility[ticker]}
    return result

if __name__ == "__main__":    
    # Fetch historical data for a list of tickers over the past year
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']  # Add more tickers as needed
    data = getStableStocks(tickers)
    print(data)
    