import os
import numpy as np

# Define the directory where your .npy files are located
directory = './prediction_data/'

# Get a list of all .npy files in the directory
files = [file for file in os.listdir(directory) if file.endswith('.npy')]

# Load all .npy files into a list
arrays = [np.load(os.path.join(directory, file)) for file in files]

# Concatenate the arrays along the first dimension
concatenated_array = np.concatenate([arrays], axis=0)

# Save the concatenated array as a new .npy file
print(concatenated_array)
np.save(os.path.join(directory, 'new_file.npy'), concatenated_array)

