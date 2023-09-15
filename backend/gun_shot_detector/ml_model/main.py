import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
import h5py

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
    mfccs_dset = hf.create_dataset("mfccs", (0, 13, MAX_LENGTH), maxshape=(None, 13, MAX_LENGTH), dtype='float32', chunks=True)
    labels_dset = hf.create_dataset("labels", (0,), maxshape=(None,), dtype=h5py.string_dtype(encoding='utf-8'), chunks=True)

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
        combined_mfccs = np.array([mfccs, augmented_mfccs]).reshape(-1, MAX_LENGTH * 13)

        # Partially fit and transform using the scaler
        scaler.partial_fit(combined_mfccs)
        scaled_mfccs = scaler.transform(combined_mfccs).reshape(-1, 13, MAX_LENGTH)

        # Append to the HDF5 dataset
        mfccs_dset.resize((idx*2)+2, axis=0)
        mfccs_dset[idx*2:idx*2+2] = scaled_mfccs

        label = os.path.basename(os.path.dirname(file))
        labels_dset.resize((idx*2)+2, axis=0)
        labels_dset[idx*2:idx*2+2] = [label, label]

print("MFCCs and labels saved to mfcc_data.h5")
print("Scaler saved to scaler.pkl")