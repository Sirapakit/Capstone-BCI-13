import mne
import mne.viz
import numpy as np
import json
 
data = open('./info_chb15_17.json')
f = json.load(data)

data_file = '../dataset/' + f['patient_ID'] + '/' + f['raw_name']
raw = mne.io.read_raw(data_file)

raw_array = raw.get_data()
raw_array = mne.filter.filter_data(raw_array, sfreq=256, l_freq=70, h_freq=1, method='iir')

seizure_event = { 'inter_ictal' : 0, 'seizure_onset' : 1, 'ictal' : 2 }
event_array = np.zeros((1,921600))

sampling_rate = 256
soz_start_sample = sampling_rate * (f['time_stamp']['start'] - 30)
start_sample = sampling_rate * (f['time_stamp']['start'])
end_sample = sampling_rate * (f['time_stamp']['end'])

event_array[0][soz_start_sample:start_sample] = seizure_event['seizure_onset']
event_array[0][start_sample:end_sample] = seizure_event['ictal']
np.append(raw_array, event_array, axis=0)

channels_number = f['channels']["number"]
new_channels_number = channels_number + 1
raw_array_with_seizure_event = np.zeros((new_channels_number, 921600))

raw_array_with_seizure_event[:channels_number][:] = raw_array
raw_array_with_seizure_event[channels_number][:] = event_array

Fp2_T8 = (f['channels']['Fp2_F8']) - 1
F8_T8 = (f['channels']['F8_T8']) - 1
Fp2_T8_channel = raw_array_with_seizure_event[Fp2_T8] 
F8_T8_channel = raw_array_with_seizure_event[F8_T8]
seizure_event_channel = raw_array_with_seizure_event[channels_number]

final_array = np.zeros((3, 921600))
final_array[0][:] = Fp2_T8_channel 
final_array[1][:] = F8_T8_channel
final_array[2][:] = seizure_event_channel 

final_array[0] = (final_array[0]-np.min(final_array[0]))/(np.max(final_array[0])-np.min(final_array[0]))
final_array[1] = (final_array[1]-np.min(final_array[1]))/(np.max(final_array[1])-np.min(final_array[1]))

data = final_array
filename = 'data_' + f['raw_name'].split('.')[0]
np.save(filename, data)