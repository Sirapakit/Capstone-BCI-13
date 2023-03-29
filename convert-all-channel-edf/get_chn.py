import mne
import mne.viz
import numpy as np

# chb = "chb01"
# data_file = '../dataset/' + chb + '/' + chb + '_03.edf'
# raw = mne.io.read_raw(data_file)
# raw_array = raw.get_data()

# print(raw.ch_names)
# print('-----------------------------------------------')
# print(f"There is {len(raw.ch_names)} channels in {chb}")
# print('-----------------------------------------------')


data_1 = np.load('./8bands-nonorm/8bands-chb03-nonorm.npy')
data_2 = np.load('./8bands-nonorm/8bands-chb03-norm.npy')

mean1 = np.mean(data_1[13*8])
mean2 = np.mean(data_2[13*8])

print(f"COEFF is {mean2/mean1}")