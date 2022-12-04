import numpy as np

path = r'./data_chb01_03.npy'
data = np.load(path)

Fp2_F8_channel = data[0]
F8_T8_channel = data[1]

np.save('Fp2_F8_channel.npy', Fp2_F8_channel)
np.save('F8_T8_channel.npy', F8_T8_channel)