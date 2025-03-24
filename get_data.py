import yfinance as yf

def fetch_stock_data():
    STOCKS = {
        "ETH": "ETH-USD",
        "BTC": "BTC-USD",
        "AMZN": "AMZN",
        "GOOG": "GOOG",
        "TSLA": "TSLA",
        "AAPL": "AAPL"
    }
    
    stock_prices = {}

    for ticker, yahoo_symbol in STOCKS.items():
        try:
            # Fetch last 14 days of data to ensure at least 7 trading days
            data = yf.download(yahoo_symbol, period="14d", interval="1d", auto_adjust=True)

            if data.empty:
                print(f"Error: No data found for {ticker}")
                continue
            
            # Ensure 'Close' is a Series (not DataFrame) before converting to a list
            closing_prices = data[["Close"]].squeeze().dropna().tolist()

            if len(closing_prices) >= 7:
                stock_prices[ticker] = closing_prices[-7:]  # Get last 7 available days
                print(f"✅ Fetched data for {ticker}: {stock_prices[ticker]}")
            else:
                print(f"⚠️ Error: Not enough trading data for {ticker}, only {len(closing_prices)} values available.")

        except Exception as e:
            print(f"❌ Error fetching data for {ticker}: {e}")
    
    return stock_prices