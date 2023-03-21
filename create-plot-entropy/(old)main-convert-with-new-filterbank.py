import mne
import mne.viz
import numpy as np
import json
from scipy import signal
from scipy.stats import mode
from scipy.stats import entropy
import os

path = '../json_convert_to_npy/chb04'
patient_chb = 'chb04'
json_filename_array = os.listdir(path)
json_filename_array.sort()

print('--------Start--------')
for index, json_filename in enumerate(json_filename_array):
    print(f'Investigating JSON: {json_filename}')

    data = open('../' + 'json_convert_to_npy/' + patient_chb + '/' + json_filename)
    f = json.load(data)

    # get edf filename from json info
    edf_name_from_json = json_filename.split("_")[1] + '_' + json_filename.split("_")[2].split('.')[0] + '.edf'
    print(f'Investigating EDF: {edf_name_from_json}')

    # Open dataset and create array name of edf files
    path_dataset = '../dataset/' + f['patient_ID']
    edf_filename_array = os.listdir(path_dataset)
    edf_filename_array.sort()

    for index, edf_filename in enumerate(edf_filename_array):
        if (json_filename.endswith('.json')):
            data_file = path_dataset + '/' + f['raw_name']
            if (edf_name_from_json == edf_filename):
                raw = mne.io.read_raw(data_file)
                raw_array = raw.get_data()

                array_length = raw_array.shape[1]
                seizure_event = { 'inter_ictal' : 0, 'seizure_onset' : 1, 'ictal' : 2 }
                event_array = np.zeros((1,array_length))

                sampling_rate = 256

                channels_number = f['channels']["number"]
                new_channels_number = channels_number + 1
                raw_array_with_seizure_event = np.zeros((new_channels_number, array_length))

                raw_array_with_seizure_event[:channels_number][:] = raw_array
                raw_array_with_seizure_event[channels_number][:] = event_array

                Fp2_T8 = (f['channels']['Fp2_F8']) - 1
                F8_T8 = (f['channels']['F8_T8']) - 1
                Fp2_T8_channel = raw_array_with_seizure_event[Fp2_T8] 
                F8_T8_channel = raw_array_with_seizure_event[F8_T8]
                seizure_event_channel = raw_array_with_seizure_event[channels_number]

                # find entropy
                
                norm_Fp2_T8_channel = (Fp2_T8_channel-np.min(Fp2_T8_channel))/(np.max(Fp2_T8_channel)-np.min(Fp2_T8_channel))

                start 
                for i in range():
                    

                entropy_Fp2_T8_channel = entropy(norm_Fp2_T8_channel)


                data_array = np.zeros((3, array_length))
                data_array[16][:] = entropy_band_Fp2_T8
                data_array[17][:] = entropy_band_F8_T8

               
                
                for i in range(16):
                    energy_array[i] = (energy_array[i]-np.min(energy_array[i]))/(np.max(energy_array[i])-np.min(energy_array[i]))

                
                data = energy_array
                save_path = './entropy/' + patient_chb
                filename = 'data_' + f['raw_name'].split('.')[0] + '_energy_v2'
                np.save(os.path.join( save_path, filename ), data)

        else: 
            print(f'-------------  No {edf_name_from_json} in dataset folder -------------')
            continue
    else:
        print(f'-------------  {json_filename} is not an edf file  -------------')
        continue
    

print('--------Stop--------')
