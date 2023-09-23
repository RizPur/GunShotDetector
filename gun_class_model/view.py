import h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

# Load data from HDF5
with h5py.File('mfcc_data.h5', 'r') as f:
    mfccs = f['mfccs'][:]
    labels = f['labels'][:]  # Assuming you also have labels stored

# Flatten the MFCCs for dimensionality reduction
mfccs_flattened = np.reshape(mfccs, (mfccs.shape[0], -1))

# Use t-SNE for dimensionality reduction
tsne = TSNE(n_components=2, random_state=0)
mfccs_2d = tsne.fit_transform(mfccs_flattened)

# Plotting
plt.figure(figsize=(10, 6))
for i, label in enumerate(np.unique(labels)):
    plt.scatter(mfccs_2d[labels == label, 0],
                mfccs_2d[labels == label, 1], label=label)
plt.legend()
plt.title('2D representation of audio samples using t-SNE')
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.show()
