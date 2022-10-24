# For elimiating warnings
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

import mne
import mne.viz
import numpy as np
import matplotlib.pyplot as plt

#Load epoched data
data_file = 'C:/Users/sirap/Desktop/BCI-y4/Capstone-BCI-13/real-time-vis/chb15_06.raw.fif'
# Read the EEG epochs:
raw = mne.io.read_raw_fif(data_file)

events = mne.find_events(raw,stim_channel='trig')
print(events)

epochs = mne.Epochs(raw, events= events,event_id=1, tmin=0, tmax=125, baseline=None)
print(epochs)

# raw.pick_channels(['F8-T8']).plot()

# epochs = mne.read_epochs(data_file, verbose='error')

# Plot of initial evoked object
# epochs.average().plot()

plt.show()