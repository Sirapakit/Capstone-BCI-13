import mne
import mne.viz
import numpy as np
import json
from scipy import signal
import os

print('--------Start--------')
data = open('./info_chb01_03.json')
f = json.load(data)

data_file = r'/Users/sirap/Documents/Capstone-BCI-13/plot-all-channels/chb01_03.edf'
raw = mne.io.read_raw(data_file)
print(raw)
print("Hello")
print(raw.ch_names)

raw_array = raw.get_data()
# raw_array = mne.filter.filter_data(raw_array, sfreq=256, l_freq=70, h_freq=1, method='iir')
# filter_5to7_Hz = [0.166797707386540, -0.0267276983200906, -0.0251359933901501, -0.0237282544477877, -0.0226758311940409, -0.0218746815950535, -0.0212708910636323, -0.0207510459663008, -0.0203443373236279, -0.0199337917859758, -0.0195667533413559, -0.0191199395846613, -0.0186487445257550, -0.0180319630065850, -0.0173374079543796, -0.0164556282656130, -0.0154715709716487, -0.0142920199176469, -0.0130180798060998, -0.0115704101194065, -0.0100598737964334, -0.00841513636515290, -0.00674936652925859, -0.00499529453304915, -0.00326420365334638, -0.00149445226578940, 0.000205031291211148, 0.00188338118154911, 0.00343537560043146, 0.00488675341753732, 0.00614748065715841, 0.00719634196411083, 0.00800530815503358, 0.00838523367967852, 0.00895215045935209, 0.00930743239165921, 0.00895215045935209, 0.00838523367967852, 0.00800530815503358, 0.00719634196411083, 0.00614748065715841, 0.00488675341753732, 0.00343537560043146, 0.00188338118154911, 0.000205031291211148, -0.00149445226578940, -0.00326420365334638, -0.00499529453304915, -0.00674936652925859, -0.00841513636515290, -0.0100598737964334, -0.0115704101194065, -0.0130180798060998, -0.0142920199176469, -0.0154715709716487, -0.0164556282656130, -0.0173374079543796, -0.0180319630065850, -0.0186487445257550, -0.0191199395846613, -0.0195667533413559, -0.0199337917859758, -0.0203443373236279, -0.0207510459663008, -0.0212708910636323, -0.0218746815950535, -0.0226758311940409, -0.0237282544477877, -0.0251359933901501, -0.0267276983200906, 0.166797707386540]

array_length = raw_array.shape[1]
seizure_event = { 'inter_ictal' : 0, 'seizure_onset' : 1, 'ictal' : 2 }
event_array = np.zeros((1,array_length))

sampling_rate = 256
soz_start_sample = sampling_rate * (f['time_stamp']['start'][0] - 30)
start_sample = sampling_rate * (f['time_stamp']['start'][0])
end_sample = sampling_rate * (f['time_stamp']['end'][0])

def box_text(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = [' '*7 + '#' + '─' * width + '#']
    for s in lines:
        res.append(' '*7 + '│' + (s + ' ' * width)[:width] + '│')
    res.append(' '*7 + '#' + '─' * width + '#')
    return '\n'.join(res)

number_of_seizure = f['number_of_seizure']
if (number_of_seizure == 0 ):
    print(box_text('NO SEIZURE DETECT'))
    np.append(raw_array, event_array, axis=0)

elif (number_of_seizure == 1):
    print(box_text(f'{str(number_of_seizure).upper()} SEIZURE DETECT'))
    event_array[0][soz_start_sample:start_sample] = seizure_event['seizure_onset']
    event_array[0][start_sample:end_sample] = seizure_event['ictal']
    np.append(raw_array, event_array, axis=0)

elif (number_of_seizure >= 2):
    print(box_text(f'{str(number_of_seizure).upper()} SEIZURE DETECT'))
    for i in range (number_of_seizure):
        event_array[0][sampling_rate * (f['time_stamp']['start'][i] - 30):
                    sampling_rate * (f['time_stamp']['start'][i])] = seizure_event['seizure_onset']
        event_array[0][sampling_rate * (f['time_stamp']['start'][i]):
                        sampling_rate * (f['time_stamp']['end'][i])] = seizure_event['ictal']
        np.append(raw_array, event_array, axis=0)

else:
    print(box_text('ERROR: WRONG NUMBER_SEIZURE'))

channels_number = f['channels']["number"]
new_channels_number = channels_number + 1
raw_array_with_seizure_event = np.zeros((new_channels_number, array_length))

raw_array_with_seizure_event[:channels_number][:] = raw_array
raw_array_with_seizure_event[channels_number][:] = event_array

# Fp2_T8 = (f['channels']['Fp2_F8']) - 1
# F8_T8 = (f['channels']['F8_T8']) - 1
# Fp2_T8_channel = raw_array_with_seizure_event[Fp2_T8] 
# F8_T8_channel = raw_array_with_seizure_event[F8_T8]
# seizure_event_channel = raw_array_with_seizure_event[channels_number]

# final_array = np.zeros((3, array_length))
# for i in range(raw_array.shape[0]):
    # final_array[0][:] = Fp2_T8_channel 
    # final_array[1][:] = F8_T8_channel
    # final_array[2][:] = seizure_event_channel 

# final_array[0][:] = signal.filtfilt(filter_5to7_Hz, 1, final_array[0][:])
# final_array[1][:] = signal.filtfilt(filter_5to7_Hz, 1, final_array[1][:])

# final_array[0] = (final_array[0]-np.min(final_array[0]))/(np.max(final_array[0])-np.min(final_array[0]))
# final_array[1] = (final_array[1]-np.min(final_array[1]))/(np.max(final_array[1])-np.min(final_array[1]))

for i in range(0, 24):
    raw_array_with_seizure_event[i] = (raw_array_with_seizure_event[i]-np.min(raw_array_with_seizure_event[i]))/(np.max(raw_array_with_seizure_event[i])-np.min(raw_array_with_seizure_event[i]))

# data = final_array
data = raw_array_with_seizure_event
# save_path = '../dataset/' + patient_chb + '/npy'
filename = 'data_' + f['raw_name'].split('.')[0]

np.save(filename + '_all_channels2', data)

print('--------Stop--------')
