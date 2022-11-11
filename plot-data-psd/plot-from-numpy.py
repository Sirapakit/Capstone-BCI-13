import numpy as np 
import mne

signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5], dtype=float)
ourier = np.fft.fft(signal)
n = signal.size
timestep = 0.1
freq = np.fft.fftfreq(n, d=timestep)
freq