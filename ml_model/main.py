import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
import h5py
import torch.nn as nn
import torch
from torch.utils.data import random_split, TensorDataset, DataLoader
import torch.optim as optim
import pickle
import torch.nn.functional as F


def extract_mfccs(y, sr):
    return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)


def augment_audio(y):
    return librosa.effects.time_stretch(y, rate=0.9)


def pad_mfcc(mfcc, max_length):
    if mfcc.shape[1] < max_length:
        padding = np.zeros((mfcc.shape[0], max_length - mfcc.shape[1]))
        mfcc = np.hstack((mfcc, padding))
    else:
        mfcc = mfcc[:, :max_length]
    return mfcc


all_files = []
for subdir, _, files in os.walk('gunshots'):
    for file in files:
        if file.endswith('.wav'):
            all_files.append(os.path.join(subdir, file))

# Determine the MAX_LENGTH for all files
all_lengths = []
for file in all_files:
    y, sr = librosa.load(file)
    mfccs = extract_mfccs(y, sr)
    all_lengths.append(mfccs.shape[1])
MAX_LENGTH = max(all_lengths)

# Create an HDF5 file to store the MFCCs and labels
with h5py.File('mfcc_data.h5', 'w') as hf:
    mfccs_dset = hf.create_dataset("mfccs", (0, 13, MAX_LENGTH), maxshape=(
        None, 13, MAX_LENGTH), dtype='float32', chunks=True)
    labels_dset = hf.create_dataset("labels", (0,), maxshape=(
        None,), dtype=h5py.string_dtype(encoding='utf-8'), chunks=True)

    scaler = StandardScaler()

    for idx, file in enumerate(all_files):
        y, sr = librosa.load(file)
        mfccs = extract_mfccs(y, sr)
        y_stretched = augment_audio(y)
        augmented_mfccs = extract_mfccs(y_stretched, sr)

        # Pad the MFCCs to the determined length
        mfccs = pad_mfcc(mfccs, MAX_LENGTH)
        augmented_mfccs = pad_mfcc(augmented_mfccs, MAX_LENGTH)

        # Reshape for scaling
        combined_mfccs = np.array(
            [mfccs, augmented_mfccs]).reshape(-1, MAX_LENGTH * 13)
        print(f"Training combined_mfccs shape: {combined_mfccs.shape}")

        # Partially fit and transform using the scaler
        scaler.partial_fit(combined_mfccs)
        scaled_mfccs = scaler.transform(
            combined_mfccs).reshape(-1, 13, MAX_LENGTH)

        # Append to the HDF5 dataset
        mfccs_dset.resize((idx*2)+2, axis=0)
        mfccs_dset[idx*2:idx*2+2] = scaled_mfccs

        label = os.path.basename(os.path.dirname(file))
        labels_dset.resize((idx*2)+2, axis=0)
        labels_dset[idx*2:idx*2+2] = [label, label]

    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

print("MFCCs and labels saved to mfcc_data.h5")
print("Scaler saved to scaler.pkl")


class AudioModel(nn.Module):
    def __init__(self, num_classes=4):
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


def train_model(model, train_loader, val_loader, device, optimizer, criterion, num_epochs=75, early_stopping_patience=5, save_path='best_model.pth'):
    """Train the model with early stopping and save the best model."""
    best_val_loss = float('inf')
    patience_counter = 0

    for epoch in range(num_epochs):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

        # Validation loss
        val_loss = 0
        model.eval()
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                outputs = model(data)
                loss = criterion(outputs, target)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)
        print(
            f"Epoch {epoch+1}/{num_epochs}, Training Loss: {loss.item()}, Validation Loss: {avg_val_loss}")

        # Save the model if validation loss has improved
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Model saved to {save_path}")
            patience_counter = 0
        else:
            patience_counter += 1

        # Early stopping
        if patience_counter >= early_stopping_patience:
            print("Early stopping triggered.")
            break

        print("model from training")
        print(model)

    return model


def test_model(audio_file_path, model_path, scaler, num_classes=4):
    # Load the audio file
    y, sr = librosa.load(audio_file_path)

    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Pad the MFCCs
    max_length = 216  # You'll need to set this to whatever value you used during training
    if mfccs.shape[1] < max_length:
        padding = np.zeros((mfccs.shape[0], max_length - mfccs.shape[1]))
        mfccs = np.hstack((mfccs, padding))
    else:
        mfccs = mfccs[:, :max_length]

    # Scale the MFCCs
    # mfccs = scaler.transform(mfccs.T).T.reshape(1, 13, max_length)

    # Reshape for scaling, similar to what you did during training
    mfccs_reshaped = mfccs.T.reshape(-1, 13 * max_length)
    # print(f"Testing mfccs_reshaped shape: {mfccs_reshaped.shape}")

    # Scale the MFCCs
    scaled_mfccs = scaler.transform(mfccs_reshaped)

    # Reshape back to original shape
    mfccs = scaled_mfccs.reshape(1, 13, max_length)

    # Convert to tensor
    mfccs_tensor = torch.tensor(mfccs).unsqueeze(0).float()

    # Load the model
    model = AudioModel(num_classes=num_classes)
    dummy_input = torch.randn(1, 1, 13, MAX_LENGTH).to(
        device)  # Replace MAX_LENGTH with the actual value
    model(dummy_input)  # This will initialize fc1
    print("model from test")
    print(model)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # Make the prediction
    with torch.no_grad():
        output = model(mfccs_tensor)

        # Convert the raw output to probabilities
        probabilities = F.softmax(output, dim=1)

        # Get the class with the highest probability
        predicted_class = torch.argmax(probabilities).item()

    # Map the prediction to the actual class name (you'll need to define this mapping)
    class_mapping = {0: 'Carbine', 1: 'Pistol', 2: 'Revolver', 3: 'Other'}
    predicted_class_name = class_mapping[predicted_class]

    print(f"The predicted class is: {predicted_class_name}")
    # Convert tensor to numpy array
    print(f"Probabilities: {probabilities.squeeze().cpu().numpy()}")


with h5py.File('mfcc_data.h5', 'r') as hf:
    data = np.array(hf['mfccs'][:])
    labels = np.array(hf['labels'][:])

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
train_data = torch.tensor(train_data).unsqueeze(1).float()
val_data = torch.tensor(val_data).unsqueeze(1).float()
test_data = torch.tensor(test_data).unsqueeze(1).float()

train_dataset = TensorDataset(train_data, torch.tensor(train_labels))
val_dataset = TensorDataset(val_data, torch.tensor(val_labels))
test_dataset = TensorDataset(test_data, torch.tensor(test_labels))

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Model Training with early stopping and saving
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AudioModel(len(unique_labels)).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 75  # Set a large number of epochs
# Stop if validation loss doesn't improve for 10 consecutive epochs
early_stopping_patience = 10
model_save_path = 'best_audio_model.pth'
train_model(model, train_loader, val_loader, device, optimizer,
            criterion, num_epochs, early_stopping_patience, model_save_path)


# Example usage
# scaler = StandardScaler()  # You'll need to load the actual scaler used during training
with open('scaler.pkl', 'rb') as f:
    loaded_scaler = pickle.load(f)
test_model('./gunshots/carbine/IP_003A_S01.wav',
           './best_audio_model.pth', loaded_scaler)


# Files that work
# './gunshots/carbine/IP_003A_S01.wav'
