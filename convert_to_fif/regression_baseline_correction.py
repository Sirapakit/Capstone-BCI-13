

import mne
import mne.viz
import numpy as np
import matplotlib.pyplot as plt

# %matplotlib inline

#Load epoched data
data_file = '../dataset/chb15/chb15_06.edf'
path = '..dataset/chb15/fif/chb15_06.raw.fif'
# raw = mne.io.read_raw(data_file)
raw = mne.io.read_raw_fif(path)

numpy_array = raw.get_data()
numpy_new = np.zeros((39, 921600))
print(type(raw.get_data()))
trig = np.zeros((1,921600))
time_stamp = { "start":1, "stop":2}
trig[0][69632] = time_stamp["start"]
trig[0][101632] = time_stamp["stop"]

# print(f'{trig[0][69630:69635]} and {trig[0][101630:101635]}')
# print(numpy_array.shape)

# np.append(numpy_array, trig,axis=0)
# print(numpy_array)
# print(numpy_array.shape)
ch_names = raw.ch_names
ch_names.append('trig') 
sfreq = raw.info["sfreq"]

numpy_new[:38][:] = numpy_array
numpy_new[38][:] = trig
# print(f"nShape new = {numpy_new}")
# print(f'{ch_names} and {sfreq}')
info = mne.create_info(ch_names, sfreq, ch_types='misc', verbose=None)

raw2 = mne.io.RawArray(numpy_new, info, first_samp=0, copy='auto', verbose=None)
print(f'Hello {raw2}')
# raw = mne.io.read_raw_fif(path)

# print(raw) 
# print(raw.info)
# print(raw.ch_names)

raw2.save("chb15_06.raw.fif")

# dummy_raw = raw.pick_channels(['--4']).get_data()
# print(dummy_raw)


# epoch1 = mne.epoch




# plt.show()