# For Load data
import glob
import os.path

# For Extracting events
import re
import mne
import numpy as np

import matplotlib.pyplot as plt

# Load data
subject_id = 1
base_path = r'../dataset'
edf_file_names = sorted(glob.glob(os.path.join(base_path, "chb{:02d}/*.edf".format(subject_id))))

def extract_data(edf_filename):
    edf = mne.io.read_raw_edf(edf_filename, stim_channel=None)
    # X = edf.get_data().astype(np.float32) * 1e6  # to mV
    X = edf.get_data() * 1e6  # to mV
    # X = X.flatten('F')
    y = np.zeros(X.shape[1], dtype=np.int64)
    # print(f'Type of X is {type(X)}') # ndarray
    assert X.shape[1] == len(y)
    return X, y


all_X = []
all_y = []
for i in edf_file_names:
    X, y = extract_data(i)
    # print(f'After extract, X is {X}')
    # print(f'After extract, type of X is {type(X)}')
    for i in X:
        for j in i:
        # print(j)
            all_X.append(j)
    all_y.append(y)


# print(f'all X is {all_X}')
print(f'y is {all_y}')
print(f'Length X is {len(all_X)}')

