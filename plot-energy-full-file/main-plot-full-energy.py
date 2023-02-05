import mne
import mne.viz
import numpy as np
import json
from matplotlib import pyplot as plt
# from scipy.stats import mode

path = '../json_convert_to_npy/chb04'
patient_chb = 'chb04'

data = open('../' + 'json_convert_to_npy/' + patient_chb + '/' + 'info_' + patient_chb + '_08.json')
f = json.load(data)
data_file = '../dataset/' + f['patient_ID'] + '/' + f['raw_name']

raw = mne.io.read_raw(data_file)
raw_array = raw.get_data()
array_length = raw_array.shape[1]
sampling_rate = 256

Fp2_T8 = (f['channels']['Fp2_F8']) - 1
F8_T8 = (f['channels']['F8_T8']) - 1
Fp2_T8_channel = raw_array[Fp2_T8] 
F8_T8_channel = raw_array[F8_T8]
print(type(F8_T8_channel))

seizure_info = { 'start': 6446, 'stop': 6557}

plt.figure(1)
plt.subplot(211)
plt.plot(Fp2_T8_channel)
plt.title('Fp2_T8_channel')
plt.grid()

plt.subplot(212)
plt.plot(F8_T8_channel)
plt.title('F8_T8_channel')
plt.grid()

xlim = {'start': 3000 - 1000, 'stop': 3500 + 1000}
plt.figure(2)
plt.subplot(211)
# plt.xlim([(xlim['start']/2) , (xlim['stop']/2) ])

start, end = 0, 512
count = 0
energy_array = []
while (end <= array_length):
    new_sub_array = F8_T8_channel[start: end]
    energy_one_part = np.sum(np.power(new_sub_array, 2))
    energy_array = np.append(energy_array, energy_one_part)
    start, end = end, end + 512
    count += 1

plt.plot(energy_array)
plt.title('Fp2_T8_channel Energy')
# Dash line for seizure
plt.vlines(seizure_info['start']/2 - 30/2, np.min(energy_array), np.max(energy_array), color='green' ,linestyle="dashed")
plt.vlines(seizure_info['start']/2 , np.min(energy_array), np.max(energy_array), color='red' ,linestyle="dashed")
plt.vlines(seizure_info['stop']/2 , np.min(energy_array), np.max(energy_array), color='red' ,linestyle="dashed")
plt.grid()

plt.subplot(212)
# plt.xlim([(xlim['start']/2) , (xlim['stop']/2) ])
start, end = 0, 512
count = 0
energy_array = []
while (end <= array_length):
    new_sub_array = F8_T8_channel[start: end]
    energy_one_part = np.sum(np.power(new_sub_array, 2))
    energy_array = np.append(energy_array, energy_one_part)
    start, end = end, end + 512
    count += 1

plt.plot(energy_array)
plt.title('F8_T8_channel Energy')
# Dash line for seizure
plt.vlines(seizure_info['start']/2 - 30/2, np.min(energy_array), np.max(energy_array), color='green' ,linestyle="dashed")
plt.vlines(seizure_info['start']/2 , np.min(energy_array), np.max(energy_array), color='red' ,linestyle="dashed")
plt.vlines(seizure_info['stop']/2 , np.min(energy_array), np.max(energy_array), color='red' ,linestyle="dashed")
plt.grid()


plt.show()