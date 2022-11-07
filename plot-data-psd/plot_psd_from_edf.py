import mne
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

myPath = r'../dataset/chb15/chb15_06.edf'
raw = mne.io.read_raw_edf(myPath, verbose=False)  # can use easy path

# Choose f8-t8 channel 
f8_t8_channel_info = raw.pick_channels(['F8-T8'])

# plot PSD from EDF
# f8_t8_channel_info.plot()
# f8_t8_channel_info.plot_psd(tmax=np.inf, fmax=128)
# plt.show()

f8_t8_array = f8_t8_channel_info.get_data()
n, array_size = f8_t8_array.shape 
# print(f8_t8_array[0])

N = array_size

yf = fft(f8_t8_array[0])
xf = fftfreq(N, 1 / 256)

fig, ax = plt.subplots()
ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.show()

# Example 
# https://mne.tools/stable/auto_tutorials/time-freq/10_spectrum_class.html#sphx-glr-auto-tutorials-time-freq-10-spectrum-class-py



