import mne
import numpy as np

# Load .edf data 
data_file = '../dataset/chb15/chb15_06.edf'
raw = mne.io.read_raw(data_file)

# Load .fif data
# path = 'C:/Users/sirap/Desktop/BCI-y4/Capstone-BCI-13/real-time-vis/chb15_06.raw.fif'
# raw = mne.io.read_raw_fif(path)

# Get data from edf as np.array
raw_array = raw.get_data()

# Create new array for epoching 
raw_array_with_trig = np.zeros((39, 921600))
# print(type(raw.get_data()))

# Create 'trigger' array 
trig = np.zeros((1,921600))
time_stamp = { 
    "soz_start":1, 
    "soz_stop":2
}
# trig[0][time_from_.txt]
trig[0][69632] = time_stamp["soz_start"]
trig[0][101632] = time_stamp["soz_stop"]

# print debug to see the array change from 0 -> 1 and 0 -> 2
print(f'{trig[0][69630:69635]} and {trig[0][101630:101635]}')

# append to create shape (39)
# print(raw_array.shape)
np.append(raw_array, trig, axis=0)
# print(raw_array.shape)

# Append 'trig' to channels
ch_names = raw.ch_names
ch_names.append('trig') 
sfreq = raw.info["sfreq"]

# Append raw.array and 'trig' channel to new_array
raw_array_with_trig[:38][:] = raw_array
raw_array_with_trig[38][:] = trig

# Should see [0.0,0,0,0,0,0,] at last channel 
# print(f"Shape new = {raw_array_with_trig}")
# Should see 'trig' channel 
# print(f'{ch_names}')

# Create info for the new_raw_data
info = mne.create_info(ch_names, sfreq, ch_types='misc', verbose=None)
raw_with_trig = mne.io.RawArray(raw_array_with_trig, info, first_samp=0, copy='auto', verbose=None)
print(f'Hello {raw_with_trig}')

filename_fif = "chb15_06.raw.fif"
raw_with_trig.save(filename_fif)

# Save to numpy file
# data = raw.get_data()
# np.save(file='my_data.npy', arr=data)

# events parameter should have 2 indices
# events[0] is 
# events[1] is 