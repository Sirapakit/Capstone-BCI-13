import mne
import mne.viz
import numpy as np
import json
from scipy import signal
import os

path = '/Users/sirap/Documents/Capstone-BCI-13/json_convert_to_npy/chb04'
patient_chb = 'chb04'
json_filename_array = ['info_chb04_08.json','info_chb04_28.json']
json_filename_array.sort()

print('--------Start--------')
for index, json_filename in enumerate(json_filename_array):
    data = open('../json_convert_to_npy/' + patient_chb + '/' + json_filename)
    # data = open('./' + patient_chb + '/' + json_filename)
    # /Users/sirap/Documents/Capstone-BCI-13/dataset
    f = json.load(data)

    data_file = '../dataset/' + f['patient_ID'] + '/' + f['raw_name']
    raw = mne.io.read_raw(data_file)

    raw_array = raw.get_data()
    # raw_array = mne.filter.filter_data(raw_array, sfreq=256, l_freq=70, h_freq=1, method='iir')
    filter_5to7_Hz = [0.166797707386540, -0.0267276983200906, -0.0251359933901501, -0.0237282544477877, -0.0226758311940409, -0.0218746815950535, -0.0212708910636323, -0.0207510459663008, -0.0203443373236279, -0.0199337917859758, -0.0195667533413559, -0.0191199395846613, -0.0186487445257550, -0.0180319630065850, -0.0173374079543796, -0.0164556282656130, -0.0154715709716487, -0.0142920199176469, -0.0130180798060998, -0.0115704101194065, -0.0100598737964334, -0.00841513636515290, -0.00674936652925859, -0.00499529453304915, -0.00326420365334638, -0.00149445226578940, 0.000205031291211148, 0.00188338118154911, 0.00343537560043146, 0.00488675341753732, 0.00614748065715841, 0.00719634196411083, 0.00800530815503358, 0.00838523367967852, 0.00895215045935209, 0.00930743239165921, 0.00895215045935209, 0.00838523367967852, 0.00800530815503358, 0.00719634196411083, 0.00614748065715841, 0.00488675341753732, 0.00343537560043146, 0.00188338118154911, 0.000205031291211148, -0.00149445226578940, -0.00326420365334638, -0.00499529453304915, -0.00674936652925859, -0.00841513636515290, -0.0100598737964334, -0.0115704101194065, -0.0130180798060998, -0.0142920199176469, -0.0154715709716487, -0.0164556282656130, -0.0173374079543796, -0.0180319630065850, -0.0186487445257550, -0.0191199395846613, -0.0195667533413559, -0.0199337917859758, -0.0203443373236279, -0.0207510459663008, -0.0212708910636323, -0.0218746815950535, -0.0226758311940409, -0.0237282544477877, -0.0251359933901501, -0.0267276983200906, 0.166797707386540]
    filter_60_Hz = [0.00442974247997994, 0.0452863192995389, -0.00437180079834794, 0.0204520237164196, 0.00173932575396934, -0.0184170404063643, -0.00543957033591100, 0.0178969390905084, 0.00945378039563676, -0.0175625058474144, -0.0141406909797757, 0.0167464899054148, 0.0194697844467726, -0.0149063245777131, -0.0251428595322106, 0.0115714914516886, 0.0306905640679811,-0.00662900704230572,-0.0355719049369381,-1.86219040961410e-05,0.0391652070589443,0.00802139786449456,-0.0409453918408629,-0.0170026255469386,0.0405516834180961,0.0263378710413190,-0.0377001390530588,-0.0353487938667215,0.0324358172968820,0.0432791141379079,-0.0249619035167384,-0.0494872827691635,0.0157113875028676,0.0535032927713320,-0.00537303142728562,0.945132189111867,-0.00537303142728562,0.0535032927713320,0.0157113875028676,-0.0494872827691635,-0.0249619035167384,0.0432791141379079,0.0324358172968820,-0.0353487938667215,-0.0377001390530588,0.0263378710413190,0.0405516834180961,-0.0170026255469386,-0.0409453918408629,0.00802139786449456,0.0391652070589443,-1.86219040961410e-05,-0.0355719049369381,-0.00662900704230572,0.0306905640679811,0.0115714914516886,-0.0251428595322106,-0.0149063245777131,0.0194697844467726,0.0167464899054148,-0.0141406909797757,-0.0175625058474144,0.00945378039563676,0.0178969390905084,-0.00543957033591100,-0.0184170404063643,0.00173932575396934,0.0204520237164196,-0.00437180079834794,0.0452863192995389,0.00442974247997994]
    
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

    Fp2_T8 = (f['channels']['Fp2_F8']) - 1
    F8_T8 = (f['channels']['F8_T8']) - 1
    ecg = (f['channels']['ecg']) - 1
    Fp2_T8_channel = raw_array_with_seizure_event[Fp2_T8] 
    F8_T8_channel = raw_array_with_seizure_event[F8_T8]
    ecg_channel = raw_array_with_seizure_event[ecg]
    seizure_event_channel = raw_array_with_seizure_event[channels_number]

    final_array = np.zeros((4, array_length))
    final_array[0][:] = Fp2_T8_channel 
    final_array[1][:] = F8_T8_channel
    final_array[2][:] = seizure_event_channel
    final_array[3][:] = ecg_channel

    final_array[0][:] = signal.filtfilt(filter_5to7_Hz, 1, final_array[0][:])
    final_array[1][:] = signal.filtfilt(filter_5to7_Hz, 1, final_array[1][:])
    final_array[3][:] = signal.filtfilt(filter_60_Hz, 1, final_array[3][:])

    final_array[0] = (final_array[0]-np.min(final_array[0]))/(np.max(final_array[0])-np.min(final_array[0]))
    final_array[1] = (final_array[1]-np.min(final_array[1]))/(np.max(final_array[1])-np.min(final_array[1]))
    final_array[3] = (final_array[3]-np.min(final_array[3]))/(np.max(final_array[3])-np.min(final_array[3]))

    data = final_array
    save_path = '../dataset/' + patient_chb + '/with-ecg'
    filename = 'data_' + f['raw_name'].split('.')[0]

    # np.savetxt("15_06.csv", data, delimiter=",")
    # np.save(filename, data)
    np.save(os.path.join( save_path, filename ), data)

print('--------Stop--------')
