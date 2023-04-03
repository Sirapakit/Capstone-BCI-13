import mne
import mne.viz
import numpy as np
import os

chb = "chb15"
data_file = '../dataset/' + chb + '/' + chb + '_02.edf'
raw = mne.io.read_raw(data_file)
raw_array = raw.get_data()

print(raw.ch_names)
print('-----------------------------------------------')
print(f"There is {len(raw.ch_names)} channels in {chb}")
print('-----------------------------------------------')
os.system('say "finish"')

data2 = np.load('./8bands-nonorm/chb15/8bands-chb15-data-crop.npy')
print(data2.shape)
print(data2[4])