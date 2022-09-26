import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import ShuffleSplit, cross_val_score

import mne
from mne import Epochs, pick_types, find_events, pick_types, set_eeg_reference
from mne.channels import read_layout
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.decoding import CSP
from mne import viz

# setup path
# myPath = r"../dataset/chb15"
myPath = r'C:/Users/sirap/Desktop/BCI-y4/Capstone-BCI-13/dataset/chb15/chb15_06.edf'
# data = os.listdir(myPath)
# dataPath = os.path.join(myPath, data[1])

# basic info
tmin, tmax = -0.1, 1.0
raw = read_raw_edf(myPath, preload=True,
                   stim_channel=None)  # can use easy path
print("-----------------------------------------------------------------")
print(f'Data type: {type(raw)}\n\n{raw}')
print('Sampling rate:', raw.info['sfreq'], 'Hz')
print(f'Size of all channels  {raw.get_data().shape}')

# Choose channel f8-t8
f8_t8_channel_info = raw.pick_channels(['F8-T8'])
print(
    f'Size of F8-T8 channel {f8_t8_channel_info.get_data().shape} and the info are\n')
print(f8_t8_channel_info)

# plot PSD
# f8_t8_channel_info.plot_psd(tmax=np.inf, fmax=128)

# Extract events from raw data
events, event_ids = mne.events_from_annotations(raw, event_id='seizure')
print(event_ids)
print(events)

# print for debug
print("Success")
