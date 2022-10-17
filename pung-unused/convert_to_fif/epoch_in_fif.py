import mne
import numpy as np

dataPath = r'../dataset/chb15/fif/chb15_06.raw.fif'

raw_fif = mne.io.read_raw_fif(dataPath,verbose=False)
channel_names = raw_fif.ch_names
print(f'Make sure we have \'trig\' at last channel, last channel:{channel_names[-1]}')

raw_fif_pick_channels = raw_fif.pick_channels(['F8-T8','FP2-F8','trig'])
print(f'Channels F8-T8 data is {raw_fif_pick_channels.get_data()}')

events = mne.find_events(raw_fif,stim_channel='trig')
events_dict = {'Ictal': 1, 'Interictal': 2}
print(f'Find event :{events}')
print(f'First event is {events[0]}')

# epochs = mne.Epochs(raw_fif, events, events_dict, tmin=0, tmax=359, proj=True, baseline=None, preload=True)
epochs = mne.Epochs(raw_fif, events, events_dict, tmin=0, tmax=100, proj=True, baseline=None, preload=True)
print(f'Epochs are : {epochs}')
# print(f'Epochs are : {epochs[1].get_data()}')

df = epochs.to_data_frame()
print(df)

# events_from_file = mne.read_events(raw_fif)
# print(events_from_file)