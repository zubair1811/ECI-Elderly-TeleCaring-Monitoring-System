# import pandas as pd
# import numpy as np
# import torch
# from torch.utils.data import DataLoader, TensorDataset
# import torch.nn as nn
#
# class LSTMRSSI(nn.Module):
#     def __init__(self, input_size, hidden_size, num_layers, num_classes):
#         super(LSTMRSSI, self).__init__()
#         self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
#         self.fc = nn.Linear(hidden_size, num_classes)
#
#     def forward(self, x):
#         out, _ = self.lstm(x)
#         out = out[:, -1, :]
#         out = self.fc(out)
#         return out
#
# # Initialize the model
# model = LSTMRSSI(input_size=1, hidden_size=50, num_layers=1, num_classes=3)
# model.load_state_dict(torch.load('lstm_rssi_model.pth'))
# model.eval()
# def predict_location(rssi_data):
#     # Convert the RSSI data to tensor and reshape for LSTM (add feature dimension)
#     rssi_tensor = torch.tensor(rssi_data, dtype=torch.float32).unsqueeze(-1).unsqueeze(0)
#
#     # Predict
#     with torch.no_grad():
#         output = model(rssi_tensor)
#         predicted_location = torch.argmax(output, dim=1)
#     return predicted_location.item()
#
# new_rssi_data = [-36]
# predicted_room = predict_location(new_rssi_data)
# print(f'Predicted Room: Room {predicted_room + 1}')

import torch
from torch import nn
import numpy as np
device = torch.device('cpu')

# Define the LSTM model for RSSI data
class LSTMRSSI(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMRSSI, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])  # Return the output of the last timestep


def load_model1(model_path, input_size=1, hidden_size=50, num_layers=1, num_classes=3, device='cpu'):
    model = LSTMRSSI(input_size, hidden_size, num_layers, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def predict1(model, rssi_data, device='cpu'):
    # Ensure rssi_data is in the correct format and convert to tensor
    if not isinstance(rssi_data, (list, np.ndarray)):
        raise TypeError("RSSI data must be a list or numpy ndarray.")

    rssi_tensor = torch.tensor([rssi_data], dtype=torch.float32).to(device).unsqueeze(-1)

    # Predict
    with torch.no_grad():
        output = model(rssi_tensor)
        predicted_location = torch.argmax(output, dim=1).item()
    return predicted_location


# # Example usage
# if __name__ == "__main__":
#     model_path = 'lstm_rssi_model.pth'
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = load_model(model_path, device=device)
#
#     new_rssi_data = [-36]
#     try:
#         predicted_room = predict_location(model, new_rssi_data, device)
#         print(f'Predicted Room: Room {predicted_room + 1}')
#     except Exception as e:
#         print(f"An error occurred: {e}")