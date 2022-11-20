from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

path = '../dataset/chb01/filterbank-npy/data_chb01_03_8bands.npy'
data = np.load(path)
print(data.shape)

fs = 256.0

for i in range(8):
    x = data[i]
    plt.grid()
    plt.title(f'Band {i+1}')
    f, Pxx_den = signal.welch(x, fs)
    plt.stem(f, Pxx_den)
    plt.show()
