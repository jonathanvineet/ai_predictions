import requests
import json

def fetch_stock_data():
    API_KEY = " H6YPXCNTFQDIXJHA"  # Replace with your actual API key
    BASE_URL = "https://www.alphavantage.co/query"
    STOCKS = ["ETH", "AMZN", "GOOG", "TSLA"]
    
    stock_prices = {}
    
    for stock in STOCKS:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock,
            "apikey": API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if "Time Series (Daily)" in data:
            time_series = data["Time Series (Daily)"]
            closing_prices = [float(time_series[date]["4. close"]) for date in sorted(time_series.keys(), reverse=True)[:7]]
            stock_prices[stock] = closing_prices
        else:
            print(f"Error fetching data for {stock}: {data}")
    
    return stock_prices

