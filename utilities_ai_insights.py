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
    Allocate investment across three stocks based on their Sharpe Ratios.
    
    stock_data: List of dictionaries containing past prices, current and predicted values.
    total_investment: Total amount to be invested.
    """
    sharpe_ratios = []
    insights = []
    
    for i, stock in enumerate(stock_data):
        log_returns = calculate_log_returns(stock["past_prices"])
        sharpe = calculate_sharpe_ratio(log_returns)
        sharpe_ratios.append(max(0, sharpe))  # Avoid negative allocations
        insights.append(f"Stock {i+1}: Sharpe Ratio = {sharpe:.2f} → {generate_insights(sharpe)}")

    # Normalize Sharpe Ratios
    sharpe_sum = sum(sharpe_ratios)
    weights = [s / sharpe_sum if sharpe_sum > 0 else 1/3 for s in sharpe_ratios]

    # Allocate funds
    allocations = [round(w * total_investment, 2) for w in weights]

    return allocations, insights
