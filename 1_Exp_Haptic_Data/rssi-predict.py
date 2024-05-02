import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn

class LSTMRSSI(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMRSSI, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)
        return out

# Initialize the model
model = LSTMRSSI(input_size=1, hidden_size=50, num_layers=1, num_classes=3)
model.load_state_dict(torch.load('lstm_rssi_model.pth'))
model.eval()
def predict_location(rssi_data):
    # Convert the RSSI data to tensor and reshape for LSTM (add feature dimension)
    rssi_tensor = torch.tensor(rssi_data, dtype=torch.float32).unsqueeze(-1).unsqueeze(0)

    # Predict
    with torch.no_grad():
        output = model(rssi_tensor)
        predicted_location = torch.argmax(output, dim=1)
    return predicted_location.item()

new_rssi_data = [-36]
predicted_room = predict_location(new_rssi_data)
print(f'Predicted Room: Room {predicted_room + 1}')