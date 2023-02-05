from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import mne


path_chb04_08 = r'/Users/sirap/Documents/Capstone-BCI-13/dataset/chb04/with-ecg/data_chb04_08.npy'
data_08 = np.load(path_chb04_08)

fs = 256.0
N = 3600 * 4 * 256
time = np.arange(N)

plt.subplot(211)
plt.grid()
plt.title('F8-T8')
f, Pxx_den = signal.welch(data_08[1], fs)
plt.semilogy(f, Pxx_den)
# plt.stem(f, Pxx_den)

plt.subplot(212)
plt.grid()
plt.title('ECG')
f, Pxx_den = signal.welch(data_08[3], fs)
plt.semilogy(f, Pxx_den)
# plt.stem(f, Pxx_den)


plt.show()