import mne
import mne.viz
import numpy as np
import json
from scipy import signal
from scipy.stats import mode
import os

path = '../json_convert_to_npy/chb06'
patient_chb = 'chb06'
json_filename_array = os.listdir(path)
json_filename_array.sort()
sampling_rate = 256

data_file = '../dataset/chb05/chb05_01.edf'
raw = mne.io.read_raw(data_file)
raw_array = raw.get_data()

print(raw.ch_names)
print(len(raw.ch_names))

print(raw_array)
print(raw_array[4].shape)


arr_2 = np.zeros((0, 3), dtype=int)
print(arr_2)  # 👉️ []
print(arr_2.shape)  # (0, 3)

# ⛔️ IndexError: index 0 is out of bounds for axis 0 with size 0
print(arr_2[0])