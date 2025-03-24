import numpy as np
def calculate_log_returns(prices):
    """Calculate log returns from historical prices."""
    return np.log(np.array(prices[1:]) / np.array(prices[:-1]))

def calculate_sharpe_ratio(log_returns, risk_free_rate=0.02):
    """Compute Sharpe Ratio given log returns."""
    mean_return = np.mean(log_returns)
    std_dev = np.std(log_returns, ddof=1)
    
    if std_dev == 0:
        return 0  # Avoid division by zero
    
    return (mean_return - risk_free_rate) / std_dev

def generate_insights(sharpe_ratio):
    """Provide insights based on Sharpe Ratio value."""
    if sharpe_ratio > 1:
        return "Excellent risk-adjusted return. Strong candidate for higher allocation."
    elif 0.5 <= sharpe_ratio <= 1:
        return "Moderate risk-adjusted return. A balanced investment choice."
    elif 0 <= sharpe_ratio < 0.5:
        return "Low risk-adjusted return. Consider investing cautiously."
    else:
        return "Negative Sharpe Ratio! Poor risk-adjusted return, indicating high volatility or losses."
def allocate_funds(stock_data, total_investment):
    """
    Allocate investment across stocks based on their Sharpe Ratios and predicted price growth.
   
    stock_data: List of dictionaries containing past prices, current and predicted values.
    total_investment: Total amount to be invested.
    """
    sharpe_ratios = []
    insights = []
   
    for stock in stock_data:
        log_returns = calculate_log_returns(stock["past_prices"])
        sharpe = calculate_sharpe_ratio(log_returns)
        sharpe_ratios.append(max(0.01, sharpe))  # Avoid zero allocation
        insights.append(f"{stock['company_name']}: Sharpe Ratio = {sharpe:.2f} → {generate_insights(sharpe)}")

    # If Sharpe Ratios are too similar, use price growth for allocation
    sharpe_sum = sum(sharpe_ratios)
    if sharpe_sum < 0.1:  # Threshold to avoid equal distribution
        predicted_growth = [
            max(0.01, (stock["predicted_price"] - stock["current_price"]) / stock["current_price"])
            for stock in stock_data
        ]
        growth_sum = sum(predicted_growth)
        weights = [g / growth_sum for g in predicted_growth] if growth_sum > 0 else [1/len(stock_data)] * len(stock_data)
    else:
        weights = [s / sharpe_sum for s in sharpe_ratios]

    # Allocate funds
    allocations = [round(w * total_investment, 2) for w in weights]
   
    return allocations, insights
