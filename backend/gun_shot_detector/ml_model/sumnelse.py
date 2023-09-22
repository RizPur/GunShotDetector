import os
import h5py
import librosa
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split

# Functions for MFCC extraction and padding


def extract_mfccs(y, sr):
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)


def pad_mfcc(mfcc, max_length):
    if mfcc.shape[1] < max_length:
        padding = np.zeros((mfcc.shape[0], max_length - mfcc.shape[1]))
        mfcc = np.hstack((mfcc, padding))
    else:
        mfcc = mfcc[:, :max_length]
    return mfcc

# Neural Network Model


class AudioModel(nn.Module):
    def __init__(self, num_classes):
        super(AudioModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.fc1_input_size = None  # Placeholder for the flattened size
        self.fc1 = None  # We'll initialize this later
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = nn.ReLU()(self.conv1(x))
        x = nn.MaxPool2d(2)(x)
        x = nn.ReLU()(self.conv2(x))
        x = nn.MaxPool2d(2)(x)

        # Dynamically compute the flattened size if not done already
        if self.fc1_input_size is None:
            self.fc1_input_size = x.shape[1] * x.shape[2] * x.shape[3]
            self.fc1 = nn.Linear(self.fc1_input_size, 128).to(x.device)

        x = x.view(x.size(0), -1)
        x = nn.ReLU()(self.fc1(x))
        x = self.fc2(x)
        return x


# Load data from mfcc_data.h5
with h5py.File('mfcc_data.h5', 'r') as hf:
    data = np.array(hf['mfccs'][:])
    labels = np.array(hf['labels'][:])

# Compute MAX_LENGTH from the loaded data
MAX_LENGTH = max([mfcc.shape[1] for mfcc in data])

# Convert labels to integers
unique_labels = list(set(labels))
label_to_int = {label: i for i, label in enumerate(unique_labels)}
labels = np.array([label_to_int[label] for label in labels])


# Splitting data into training, validation, and testing
train_size = int(0.7 * len(data))
val_size = int(0.1 * len(data))
test_size = len(data) - train_size - val_size
train_data, val_data, test_data = random_split(
    data, [train_size, val_size, test_size])
train_labels, val_labels, test_labels = random_split(
    labels, [train_size, val_size, test_size])

# Convert the data to tensors and add a channel dimension
train_data = torch.tensor(np.array(train_data)).unsqueeze(1).float()
val_data = torch.tensor(np.array(val_data)).unsqueeze(1).float()
test_data = torch.tensor(np.array(test_data)).unsqueeze(1).float()


train_dataset = TensorDataset(train_data, torch.tensor(train_labels))
val_dataset = TensorDataset(val_data, torch.tensor(val_labels))
test_dataset = TensorDataset(test_data, torch.tensor(test_labels))

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Initialize and load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AudioModel(len(unique_labels)).to(device)

# Run a dummy input through the model to initialize all layers
dummy_input = torch.randn(1, 1, 13, MAX_LENGTH).to(device)
model(dummy_input)

# Now load the model weights
model.load_state_dict(torch.load('best_audio_model.pth'))
model.eval()


def predict_from_file(filename):
    y, sr = librosa.load(filename, sr=44100)  # Load the audio file
    mfccs = extract_mfccs(y, sr)
    mfccs = pad_mfcc(mfccs, MAX_LENGTH)
    mfccs_tensor = torch.tensor(mfccs).unsqueeze(
        0).unsqueeze(0).float().to(device)
    return model(mfccs_tensor)


# audio_file_path = "/Users/dawei/Documents/AI\ Hackathon/ml_model/Gun\ audio/AK-47/1\ (1).wav"
audio_file_path = "./Gun audio/AK-47/1 (1).wav"
model_output = predict_from_file(audio_file_path)
# Get the index of the maximum value in the output tensor
predicted_index = torch.argmax(model_output).item()

# Map the index to the corresponding gun type
predicted_gun_type = unique_labels[predicted_index]

print(f"Predicted gun type: {predicted_gun_type}")
print(model_output)
