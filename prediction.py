from utilities_model import load_scaler, load_model, predict_single

# Load models and scalers
model_eth = load_model(r"assests/models/model_eth.pt")
scaler_eth = load_scaler(r"assests/scalers/minmax_scaler_eth.pkl")

model_amazon = load_model(r"assests/models/model_amazon.pt")
scaler_amazon = load_scaler(r"assests/scalers/minmax_scaler_amazon.pkl")

model_google = load_model(r"assests/models/model_google.pt")
scaler_google = load_scaler(r"assests/scalers/minmax_scaler_google.pkl")

model_tsla = load_model(r"assests/models/model_tsla.pt")
scaler_tsla = load_scaler(r"assests/scalers/minmax_scaler_tsla.pkl")

model_apple = load_model(r"assests/models/model_apple.pt")
scaler_apple = load_scaler(r"assests/scalers/minmax_scaler_apple.pkl")

model_btc = load_model(r"assests/models/model_btc.pt")
scaler_btc = load_scaler(r"assests/scalers/minmax_scaler_btc.pkl")

def prediction(stock_values, ticker):
    if len(stock_values) != 7:
        print("Error: You must provide exactly 7 stock values.")
        exit(1)

    # Select model/scaler based on ticker symbol
    model_scaler_map = {
        "ETH": (model_eth, scaler_eth),
        "AMZN": (model_amazon, scaler_amazon),
        "GOOG": (model_google, scaler_google),
        "TSLA": (model_tsla, scaler_tsla),
        "AAPL": (model_apple, scaler_apple),
        "BTC": (model_btc, scaler_btc)
    }

    if ticker not in model_scaler_map:
        print("Ticker not recognized. Please try again.")
        exit(1)
    
    model, scaler = model_scaler_map[ticker]

    # Use the model and scaler to predict the next day's stock price
    predicted_price = predict_single(model, stock_values, scaler)
    return predicted_price