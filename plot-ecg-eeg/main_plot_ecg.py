import matplotlib.pyplot as plt
import numpy as np

path_chb04_08 = r'/Users/sirap/Documents/Capstone-BCI-13/dataset/chb04/with-ecg/data_chb04_08.npy'
path_chb04_28 = r'/Users/sirap/Documents/Capstone-BCI-13/dataset/chb04/with-ecg/data_chb04_28.npy'
data_08 = np.load(path_chb04_08)
data_28 = np.load(path_chb04_28)
# ECG is at last channel

data_08_info = {
        "start": [6446],
        "end": [6557]
    }

data_28_info = {
        "start": [1679, 3782],
        "end": [1781, 3898]
    }

fs = 256.0
N = 3600 * 4 * 256
time = np.arange(N)

plt.subplot(311)
plt.tight_layout(h_pad=2)
plt.grid()
plt.xlim([6200 * 256, 6800 * 256])
plt.vlines((data_08_info['start'][0] - 30) * 256, -0.002, 1, color='green', linestyle="dashed")
plt.vlines(data_08_info['start'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
plt.vlines(data_08_info['end'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
plt.title('Fp2_T8_channel')
plt.plot(data_08[0])

plt.subplot(312)
plt.tight_layout(h_pad=2)
plt.grid()
plt.xlim([6200 * 256, 6800 * 256])
plt.vlines((data_08_info['start'][0] - 30) * 256, -0.002, 1, color='green', linestyle="dashed")
plt.vlines(data_08_info['start'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
plt.vlines(data_08_info['end'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
plt.title('F8_T8_channel')
plt.plot(data_08[1])

plt.subplot(313)
plt.tight_layout(h_pad=2)
plt.grid()
plt.xlim([6200 * 256, 6800 * 256])
plt.vlines((data_08_info['start'][0] - 30) * 256, -0.002, 1, color='green', linestyle="dashed")
plt.vlines(data_08_info['start'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
plt.vlines(data_08_info['end'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")

plt.xlim([1000 * 256, 1010 * 256])
plt.ylim([0.3, 0.7])

plt.title('ECG')
plt.plot(data_08[3])

plt.show()
