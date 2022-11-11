import mne
import mne.viz
import numpy as np
import pandas as pd
import csv


# Load .edf data
data_file = '/Users/sirap/Documents/Capstone-BCI-13/convert_to_npy/input57hz0pad.csv'
arr = np.loadtxt(data_file,delimiter=",")
print(type(arr))
# # Get data from edf as np.array
# raw_array = raw.get_data()
# # Filter l=70, h=1
# raw_array = mne.filter.filter_data(raw_array, sfreq=256, l_freq=70, h_freq=1, method='iir')

# # Create event array and dict for event array
# seizure_event = { "inter_ictal" : 0, "seizure_onset" : 1, "ictal" : 2 }
# event_array = np.zeros((1,921600))

# # Assign value to event_array according to summary.txt
# event_array[0][61952:69632] = seizure_event["seizure_onset"]
# # 242 * 256 = 61952   # 272 * 256 = 69631
# event_array[0][69632:101633] = seizure_event["ictal"]
# # 272 * 256 = 69631   # 397 * 256 = 101632
# # print(f'Check event_array {event_array[0][60000:610002]}')

# # Append to raw_array
# np.append(raw_array, event_array, axis=0)

# # Create new array with 39 channels
# raw_array_with_seizure_event = np.zeros((39, 921600))

# # Append raw_array and seizure_event channel to raw_array_with_seizure_event
# raw_array_with_seizure_event[:38][:] = raw_array
# raw_array_with_seizure_event[38][:] = event_array
# # print(f'Check event_array {raw_array_with_seizure_event}')
# # print(f'Shape is {raw_array_with_seizure_event.shape}')

# # Pick 3 channels to create .csv
# Fp2_T8_channel = raw_array_with_seizure_event[19] 
# F8_T9_channel = raw_array_with_seizure_event[20]
# seizure_event_channel = raw_array_with_seizure_event[38]

# final_array = np.zeros((3, 921600))
# final_array[0][:] = Fp2_T8_channel
# final_array[1][:] = F8_T9_channel
# final_array[2][:] = seizure_event_channel 

# final_array[0] = (final_array[0]-np.min(final_array[0]))/(np.max(final_array[0])-np.min(final_array[0]))
# final_array[1] = (final_array[1]-np.min(final_array[1]))/(np.max(final_array[1])-np.min(final_array[1]))

# # print max, min
# print(np.max(final_array[0]))
# print(np.min(final_array[0]))
# print(np.max(final_array[1]))
# print(np.min(final_array[1]))

# # Create .csv with pd 
# df = pd.DataFrame(final_array.transpose(), columns=['Fp2-T8', 'F8-T8', 'event'])
# df.to_csv('chb15_06.csv')


