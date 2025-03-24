import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.nn import MSELoss

import numpy as np
import joblib

from copy import deepcopy as dc
from LSTM_architecture import LSTM

def load_scaler(path):
  scaler = joblib.load(path)
  return scaler

def load_model(path, device="cpu"):
  model = LSTM(1, 4, 1).to(device)
  checkpoint = torch.load(path, weights_only=True, map_location=torch.device('cpu'))
  model.load_state_dict(checkpoint['model_state_dict'])
  model.eval()
  return model

def predict_single(model, last_7_values, scaler, device="cpu"):
    """
    Predicts the next value using the trained LSTM model given the last 7 values.

    Args:
        model: Trained LSTM model
        last_7_values: Last 7 time steps (1D array or list)
        scaler: MinMaxScaler used for scaling during training
        device: 'cuda' or 'cpu'

    Returns:
        next_pred (float): The predicted next value (in original scale)
    """
    # Convert to numpy array and reshape for scaler
    dummy = np.zeros(8)
    dummy[1:] = last_7_values
    last_7_values = np.array(dummy).reshape(1, -1)

    # Scale the input using the same MinMaxScaler
    scaled_input = scaler.transform(last_7_values)
    scaled_input = scaled_input[:,1:]
    # Reshape to match LSTM input format (batch_size=1, lookback=7, features=1)
    scaled_input = scaled_input.reshape(1, 7, 1)

    # Convert to PyTorch tensor
    X_input = torch.tensor(scaled_input, dtype=torch.float32).to(device)

    # Get the prediction
    with torch.no_grad():
        predicted = model(X_input).to('cpu').numpy()  # Move to CPU and convert to NumPy

    # Flatten the predicted output
    predicted_value = predicted.flatten()[0]

    # Create a dummy array to inverse transform
    dummies = np.zeros((1, 8))  # Shape (1, lookback+1)
    dummies[:, 0] = predicted_value

    # Inverse transform to get the original scale
    dummies = scaler.inverse_transform(dummies)

    # Extract the final predicted value
    next_pred = dc(dummies[:, 0][0])

    return next_pred

