import numpy as np

path = r'/Users/sirap/Documents/Capstone-BCI-13/create_filterbank/mock/data_chb01_03_16energu.npy'
energy = np.load(path)

print(energy)
print(energy[0].shape)