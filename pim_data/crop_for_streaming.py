import numpy as np


data1 = np.load('../convert-all-channel-edf/8bands-nonorm/chb06/8bands-chb06-data-crop.npy')

chn1 = data1[7]
chn2 = data1[11]
chn3 = data1[16]
chn4 = data1[20]

data_final = np.vstack((chn1, chn2, chn3, chn4))
np.save("chb06-8coeff.npy", data_final)

# check = np.load('./chb17-8coeff.npy')
# print(check.shape)
