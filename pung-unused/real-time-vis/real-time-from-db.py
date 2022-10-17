import os
import numpy as np
import matplotlib.pyplot as plt
import mne

raw = mne.io.read_raw_edf('../dataset/chb15/chb15_06.edf')
raw.crop(tmax=10)

n_time_samps = raw.n_times
time_secs = raw.times
ch_names = raw.ch_names
n_chan = len(ch_names)

print()
print('the (cropped) sample data object has {} time samples and {} channels.'
      ''.format(n_time_samps, n_chan))
print(f'The last time sample is at {time_secs[-1]} seconds.')
print(f"The first few channel names are {', '.join(ch_names[:3])}.")
print(f"The channel names are {ch_names}.")
print()

# plt.savefig('foo2.png')

# raw.pick_channels(['F8-T8']).crop(tmin=0.00, tmax=1.00).plot()
# raw.pick_channels(['F8-T8']).crop(tmin=1.00, tmax=2.25).plot()
raw.plot()

plt.show()


print("Success")
