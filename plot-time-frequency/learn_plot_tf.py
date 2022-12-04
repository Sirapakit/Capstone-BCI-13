import numpy as np
import matplotlib.pyplot as plot
from numpy.fft import fft


fs = 50
ts = 1/fs
t = np.arange(0, 1, ts)

sine = np.sin(2 * np.pi * 5 * t) + 2 * np.cos(2 * np.pi * 10 * t)

plot.figure(1)
plot.subplot(211)
plot.ylabel("Amplitude")
plot.plot(t,sine)

plot.subplot(212)
y = fft(sine)
print(len(y))
plot.plot(abs(y))
plot.xlim(0, 25)

plot.figure(2)
plot.subplot(211)
NFFT = 50
plot.specgram(sine, NFFT=NFFT, Fs=fs, noverlap=10)

plot.subplot(212)
NFFT = 200
plot.specgram(sine, NFFT=NFFT, Fs=fs, noverlap=10)


plot.show()