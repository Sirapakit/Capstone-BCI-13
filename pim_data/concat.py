import numpy as np


data1 = np.load('../convert-all-channel-edf/8bands-nonorm/chb03/8bands-chb03-data-crop.npy')

chn1 = data1[5]
chn2 = data1[7]
chn3 = data1[10]
chn4 = data1[12]

data_final = np.vstack((chn1, chn2, chn3, chn4))
# np.save("chb03-8coeff.npy", data_final)

check = np.load('./chb03-8coeff.npy')
print(check.shape)
