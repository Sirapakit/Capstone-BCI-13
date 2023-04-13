import numpy as np

data_load = np.load('./chb03/chb03-8coeff.npy')
print(data_load.shape)

start_sample = 77312
stop_sample = 105984

data_cropped = data_load[:, start_sample:stop_sample]
print(data_cropped.shape)

np.save("chb03-8coeff-seizure.npy", data_cropped)