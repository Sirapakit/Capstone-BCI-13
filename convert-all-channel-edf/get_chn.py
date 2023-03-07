import mne
import mne.viz
import numpy as np

data_file = '../dataset/chb13/chb13_19.edf'
raw = mne.io.read_raw(data_file)
raw_array = raw.get_data()

print(raw.ch_names)
print(len(raw.ch_names))

print(raw_array)
print(raw_array[4].shape)
