from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import mne

myPath = r'../dataset/chb15/chb15_06.edf'
raw = mne.io.read_raw_edf(myPath, verbose=False)  # can use easy path

f8_t8_channel_info = raw.pick_channels(['F8-T8'])
data1 = f8_t8_channel_info.get_data() 

path = r'/Users/sirap/Documents/Capstone-BCI-13/json_convert_to_npy/data_chb15_06_final2.npy'
data2 = np.load(path)
print(data2)
# print(data)
# fs = 256.0
# N = 100*256
# time = np.arange(N)
# x = f8_t8_array[0][272*256:372*256]
# print(x.shape)

# f, Pxx_den = signal.periodogram(x, fs)
# plt.semilogy(f, Pxx_den)
# plt.grid()
# plt.xlabel('frequency [Hz]')
# plt.ylabel('PSD [V**2/Hz]')
# plt.show()

fs = 256.0
x11 = data1[0][0*256:272*256]
x12 = data2[0][0*256:272*256]
plt.subplot(311)
plt.tight_layout(h_pad=2)
plt.grid()
# plt.xlim([1, 500])
# plt.ylim([1e-15, 1e-9])
plt.title('Before Seizure Period')
# f, Pxx_den = signal.periodogram(x, fs)
f, Pxx_den = signal.welch(x12[0:1000], fs)
# plt.semilogy(f, Pxx_den)
plt.stem(f, Pxx_den)
# plt.plot(x11, color='r', label='raw')
# plt.plot(x12, color='g', label='filtered')


# x2 = f8_t8_array[0][242*256:272*256]
# x2 = data[0][0*256:272*256]
x21 = data1[0][242*256:272*256]
x22 = data2[0][242*256:272*256]
plt.subplot(312)
plt.tight_layout(h_pad=2)
plt.grid()
# plt.xlim([1, 500])
# plt.ylim([1e-15, 1e-9])
plt.title('Seizure Onset Period')
# f2, Pxx_den2 = signal.periodogram(x2, fs)
f2, Pxx_den2 = signal.welch(x22[0:1000], fs)
# plt.semilogy(f2, Pxx_den2)
plt.stem(f2, Pxx_den2)
# plt.plot(x2)
# plt.plot(x21, color='r', label='raw')
# plt.plot(x22, color='g', label='filtered')


# x3 = f8_t8_array[0][272*256:397*256]
# x3 = data[0][0*256:272*256]
x31 = data1[0][272*256:397*256]
x32 = data2[0][272*256:397*256]
plt.subplot(313)
plt.tight_layout(h_pad=2)
plt.grid()
# plt.xlim([1, 500])
# plt.ylim([1e-15, 1e-9])
plt.title('Seizure Period')
# f3, Pxx_den3 = signal.periodogram(x3, fs)
f3, Pxx_den3 = signal.welch(x32[0:1000], fs)
# plt.semilogy(f3, Pxx_den3)
plt.stem(f3, Pxx_den3)
# plt.plot(x3)
# plt.plot(x31, color='r', label='raw')
# plt.plot(x32, color='g', label='filtered')



plt.show()
