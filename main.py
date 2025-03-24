from waitress import serve
import json
import socket
from flask import Flask, jsonify
from flask_cors import CORS
from get_data import fetch_stock_data  # Import the function to fetch stock data
from prediction import prediction
from market_news import get_news_sentiment
from utilities_ai_insights import calculate_log_returns, calculate_sharpe_ratio, generate_insights, allocate_funds

app = Flask(__name__)
CORS(app)

def analyze_stocks(stock_prices, total_investment=10000):
    stocks = {
        "ETH": "ethereum",
        "AMZN": "amazon",
        "GOOG": "google",
        "TSLA": "tesla"
    }

    stock_data = []
    for ticker, company_name in stocks.items():
        last_7_prices = stock_prices.get(ticker, [])
        if len(last_7_prices) != 7:
            return {"error": f"Invalid data for {ticker}. Expected 7 price values."}

        predicted_price = prediction(last_7_prices, ticker)
        market_sentiment, sentiment_counts = get_news_sentiment(company_name)
        log_returns = calculate_log_returns(last_7_prices)
        sharpe_ratio = calculate_sharpe_ratio(log_returns)
        insight = generate_insights(sharpe_ratio)

        decision = "BUY" if sharpe_ratio > 1 and market_sentiment == "Bullish (Positive)" else \
                   "HOLD" if 0.5 <= sharpe_ratio <= 1 and market_sentiment in ["Bullish (Positive)", "Neutral"] else "SELL"
        confidence = "High" if decision == "BUY" else "Medium" if decision == "HOLD" else "Low"

        stock_data.append({
            "ticker": ticker,
            "company_name": company_name,
            "past_prices": last_7_prices,
            "current_price": last_7_prices[-1],
            "predicted_price": predicted_price,
            "decision": decision,
            "confidence": confidence,
            "market_sentiment": market_sentiment,
            "sentiment_counts": sentiment_counts,
            "sharpe_ratio": sharpe_ratio,
            "insight": insight
        })
    
    allocations, _ = allocate_funds(stock_data, total_investment)
    results = {}
    for i, sd in enumerate(stock_data):
        results[sd["company_name"]] = {
            "CompanyName": sd["company_name"],
            "InvestmentDecision": sd["decision"],
            "MarketAnalysis": {
                "Sentiment": f"{sd['market_sentiment']}, Insight: {sd['insight']}",
                "SharpeRatio": round(sd["sharpe_ratio"], 2)
            },
            "ConfidenceLevel": sd["confidence"],
            "NextDayPredictedPrice": sd["predicted_price"],
            "AllocatedFunds": f"${allocations[i]}"
        }
    return results


@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        stock_prices = fetch_stock_data()
        result = analyze_stocks(stock_prices)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>Stock Analysis API</h1>
    <p>Send a get request to /analyze with stock price data to get investment recommendations.</p>
    </pre>
    '''
host = "0.0.0.0"
port = 5000
app.run(debug=True, host='0.0.0.0', port=5000)
local_ip = socket.gethostbyname(socket.gethostname())
print(f"Server running on: http://{local_ip}:{port}")
serve(app, host=host, port=port)
