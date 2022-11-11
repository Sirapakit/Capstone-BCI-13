import mne
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

myPath = r'../dataset/chb15/chb15_06.edf'
raw = mne.io.read_raw_edf(myPath, verbose=False)  # can use easy path

# Choose f8-t8 channel 
f8_t8_channel_info = raw.pick_channels(['F8-T8'])

# plot PSD from EDF
# f8_t8_channel_info.plot()
# f8_t8_channel_info.plot_psd(tmax=np.inf, fmax=128)
# plt.show()




# Example 
# https://mne.tools/stable/auto_tutorials/time-freq/10_spectrum_class.html#sphx-glr-auto-tutorials-time-freq-10-spectrum-class-py



