from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

path_old = "/Users/sirap/Documents/Capstone-BCI-13/create_filterbank/energy_bands/chb04/data_chb04_09_energy.npy"
path_v2 = "/Users/sirap/Documents/Capstone-BCI-13/create_new_filterbank/new_energy_bands/chb15/data_chb15_06_energy_v2.npy"
data_old = np.load(path_old)
data_v2 = np.load(path_v2)


fs = 256.0

for i in range(8):
    x = data_v2[i]
    plt.grid()
    plt.title(f'Band {i+1}')
    f, Pxx_den = signal.welch(x, fs)
    plt.stem(f, Pxx_den)
    plt.show()


# Old vs New
# for i in range(8):
#     x_old = data_old[i]
#     x_v2 = data_v2[i]
#     plt.grid()
#     plt.title(f'Energy Band {i+1}')
#     plt.plot(x_old, color='g', label='Old')
#     plt.plot(x_v2, color='r', label='New')
#     plt.title("Old and New Filterbank")
#     plt.legend()
#     plt.show()

