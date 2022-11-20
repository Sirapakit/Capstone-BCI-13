from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import mne

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

# plt.subplot(311)
# plt.tight_layout(h_pad=2)
# plt.grid()
# # plt.xlim([data_08_info['start'][0] - 30 - 300, data_08_info['end'][0] + 300])
# # plt.ylim([0.35, 0.45])
# plt.vlines(data_08_info['start'][0], -0.002, data_08[3][data_08_info['start'][0]], linestyle="dashed")
# plt.vlines(data_08_info['end'][0], -0.002, data_08[3][data_08_info['start'][0]], linestyle="dashed")
# plt.title('Fp2_T8_channel')
# plt.plot(time, data_08[0])

plt.subplot(211)
plt.tight_layout(h_pad=2)
plt.grid()
plt.xlim([6000 * 256, 7000 * 256])
plt.vlines(data_08_info['start'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
plt.vlines(data_08_info['end'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
# plt.vlines(data_28_info['start'][0] * 256, -0.002, 1, color='red', linestyle="dashed")
# plt.vlines(data_28_info['end'][0] * 256, -0.002, 1, color='red', linestyle="dashed")
plt.title('F8_T8_channel')
plt.plot(data_08[1])
# plt.plot(data_28[1])


plt.subplot(212)
plt.tight_layout(h_pad=2)
plt.grid()
plt.xlim([6000 * 256, 7000 * 256])
plt.vlines(data_08_info['start'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
plt.vlines(data_08_info['end'][0] * 256, -0.002, 1, color='red' ,linestyle="dashed")
# plt.vlines(data_28_info['start'][0] * 256, -0.002, 1, color='red', linestyle="dashed")
# plt.vlines(data_28_info['end'][0] * 256, -0.002, 1, color='red', linestyle="dashed")
plt.title('ECG')
plt.plot(data_08[3])
# plt.plot(data_28[3])

plt.show()
