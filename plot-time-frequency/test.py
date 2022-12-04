import numpy as np
import pylab as plt

# generate a 1kHz sine wave
fs = 32e3
t = np.arange(0, 15, 1.0/fs)
f0 = 1e3
A = 1
x = A*np.sin(2*np.pi*f0*t)

fig, ax = plt.subplots()
cmap = plt.get_cmap('viridis')
vmin = 20*np.log10(np.max(x)) - 40  # hide anything below -40 dBc
cmap = 'seismic'

NFFT = 256
pxx,  freq, t, cax = ax.specgram(x/(NFFT/2), Fs=fs, mode='magnitude',
                                 NFFT=NFFT, noverlap=NFFT/2,
                                 vmin=vmin, cmap=cmap,
                                 window=plt.window_none)
fig.colorbar(cax)

print(np.max(pxx)) # should match A
plt.show()