# import torch
# from torch.utils.data import DataLoader, TensorDataset, random_split
# import numpy as np
# from torch import nn
# import torch.optim as optim
# from sklearn.metrics import accuracy_score
# device = torch.device('cpu')
# # Parameters
# sequence_length = 1
# # Example Model (simple LSTM model for demonstration)
# class LSTMModel(torch.nn.Module):
#     def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
#         super(LSTMModel, self).__init__()
#         self.lstm = torch.nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
#         self.fc = torch.nn.Linear(hidden_dim, output_dim)
#
#     def forward(self, x):
#         out, _ = self.lstm(x)
#         out = self.fc(out[:, -1, :])  # Get the last time step output
#         return out
#
# # Initialize the model and move it to the device
# model = LSTMModel(input_dim=6, hidden_dim=100, num_layers=1, output_dim=3)
# model = model.to(device)
# # Example of how to load and use the model for predictions
# model.load_state_dict(torch.load('best_model.pth'))
# model.eval()  # Make sure to set the model to evaluation mode
#
#
# # Predicting on new data
# def predict(data):
#     # Reshape data to (1, sequence_length, number_of_features)
#     # Check if data length matches the sequence length used during training
#     if len(data) != sequence_length:
#         print("Data length does not match the expected sequence length.")
#         return None
#
#     # Ensure the data is a 2D array with sequence length and number of features
#     data = np.array([data])  # Reshape data to (1, sequence_length, number_of_features)
#     data = torch.tensor(data, dtype=torch.float32).to(device)  # Convert to tensor and send to device
#     print(data)
#
#     with torch.no_grad():
#         output = model(data)
#         print(output)
#         predicted_class = output.argmax(dim=1)
#     return predicted_class.item()
#
#
# # # Example usage
# # new_data = np.random.rand(1, 6)  # Ensure this matches your training data's sequence length and feature count
# # print(new_data)
# # prediction = predict(new_data)
# # print(f'Predicted Class: {prediction}')
import torch
import numpy as np
from torch import nn

# Parameters
device = torch.device('cpu')
sequence_length = 1


class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


def load_model2(model_path, input_dim=6, hidden_dim=100, num_layers=1, output_dim=3):
    model = LSTMModel(input_dim, hidden_dim, num_layers, output_dim)
    model.load_state_dict(torch.load(model_path))
    model.to(device)
    model.eval()
    return model


def predict2(model, data):
    if len(data) != sequence_length:  # Ensure correct data length
        raise ValueError("Data length does not match the expected sequence length.")
    data = np.array([data], dtype=np.float32)
    data_tensor = torch.tensor(data).to(device)

    with torch.no_grad():
        output = model(data_tensor)
        predicted_class = output.argmax(dim=1).item()
    return predicted_class


# # Example usage
# if __name__ == "__main__":
#     model_path = 'best_model.pth'
#     model = load_model(model_path)
#     test_data = [0.5, 0.2, 0.3, 0.4, 0.5, 0.6]  # Example data
#     try:
#         result = predict(model, test_data)
#         print(f"Predicted class: {result}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
