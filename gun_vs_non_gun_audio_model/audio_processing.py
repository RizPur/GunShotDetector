import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import gc

BATCH_SIZE = 20  # Adjust based on your system's memory


def load_audio_data_from_directory(directory, batch_size=BATCH_SIZE):
    batch_audio_data = []
    batch_labels = []
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                y, sr = librosa.load(os.path.join(subdir, file))
                batch_audio_data.append((y, sr))
                # Assuming the directory name is the label
                batch_labels.append(subdir.split('/')[-1])
                if len(batch_audio_data) == batch_size:
                    yield batch_audio_data, batch_labels
                    batch_audio_data = []
                    batch_labels = []
    if batch_audio_data:
        yield batch_audio_data, batch_labels


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


def process_batch(batch_audio_data):
    mfccs_list = []
    augmented_mfccs_list = []
    for y, sr in batch_audio_data:
        mfccs = extract_mfccs(y, sr)
        mfccs_list.append(mfccs)
        y_stretched = augment_audio(y)
        augmented_mfccs = extract_mfccs(y_stretched, sr)
        augmented_mfccs_list.append(augmented_mfccs)
    return mfccs_list, augmented_mfccs_list


all_mfccs = []
all_labels = []
scaler = StandardScaler()

# Determine the MAX_LENGTH once for all batches
all_lengths = [mfcc.shape[1] for audio_data_batch, _ in load_audio_data_from_directory(
    'gunshots') for mfcc in [extract_mfccs(y, sr) for y, sr in audio_data_batch]]
MAX_LENGTH = max(all_lengths)

# Process and scale data
for batch_audio_data, batch_labels in load_audio_data_from_directory('gunshots'):
    mfccs_list, augmented_mfccs_list = process_batch(batch_audio_data)
    mfccs_list = [pad_mfcc(mfcc, MAX_LENGTH) for mfcc in mfccs_list]
    augmented_mfccs_list = [pad_mfcc(mfcc, MAX_LENGTH)
                            for mfcc in augmented_mfccs_list]

    # Combine original and augmented MFCCs and reshape for scaling
    combined_mfccs = np.array(
        mfccs_list + augmented_mfccs_list).reshape(-1, MAX_LENGTH * 13)

    # Partially fit and transform using the scaler
    scaler.partial_fit(combined_mfccs)
    scaled_mfccs = scaler.transform(combined_mfccs).reshape(-1, 13, MAX_LENGTH)

    all_mfccs.extend(scaled_mfccs)
    # Labels are duplicated due to augmentation
    all_labels.extend(batch_labels + batch_labels)

    # Clean up to free memory
    del batch_audio_data, batch_labels, mfccs_list, augmented_mfccs_list, combined_mfccs, scaled_mfccs
    gc.collect()

X_train, X_val, y_train, y_val = train_test_split(
    all_mfccs, all_labels, test_size=0.2, random_state=42)
print('X_train shape:', np.array(X_train).shape)
print('X_val shape:', np.array(X_val).shape)
print('y_train shape:', len(y_train))
print('y_val shape:', len(y_val))
