import mne
import numpy as np
import json
import os

# Change Path for each patient
path = '../../json_convert_to_npy/chb06'
patient_chb = 'chb06'
json_filename_array = os.listdir(path)
json_filename_array.sort()
sampling_rate = 256

# Get chn first
ch_names = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8-0', 'P8-O2', 'FZ-CZ', 'CZ-PZ', 'P7-T7', 'T7-FT9', 'FT9-FT10', 'FT10-T8', 'T8-P8-1']
print(f'Channels name are {ch_names}')
print(f'There are {len(ch_names)} channels')
print(f'First channel is {ch_names[0]}')

print('--------Start--------')
for index, json_filename in enumerate(json_filename_array):
    print(f'Investigating JSON: {json_filename}')

    # Open json data
    data = open('../../' + 'json_convert_to_npy/' + patient_chb + '/' + json_filename)
    f = json.load(data)

    # get edf filename from json info
    edf_name_from_json = json_filename.split("_")[1] + '_' + json_filename.split("_")[2].split('.')[0] + '.edf'
    print(f'Investigating EDF: {edf_name_from_json}')

    # Open dataset and create array name of edf files
    path_dataset = '../../dataset/' + f['patient_ID']
    edf_filename_array = os.listdir(path_dataset)
    edf_filename_array.sort()

    # Create empty array varialbe for concat file
    for i in range(len(ch_names)): 
        exec(f"main_array_channel_{i} = np.array([])") 
        
# Looping through every files in json_info/chbxx/info_xx_xx.json
for index, json_filename in enumerate(json_filename_array):
    print(f'Investigating JSON: {json_filename}')

    # Read JSON data
    data = open('../../' + 'json_convert_to_npy/' + patient_chb + '/' + json_filename)
    f = json.load(data)

    # Get edf filename from json info
    edf_name_from_json = json_filename.split("_")[1] + '_' + json_filename.split("_")[2].split('.')[0] + '.edf'
    print(f'Investigating EDF: {edf_name_from_json}')

    # Open dataset and create array name of edf files
    path_dataset = '../../dataset/' + f['patient_ID']
    edf_filename_array = os.listdir(path_dataset)
    edf_filename_array.sort()

    # Looping through every files in dataset/chbxx/chbxx_xx.edf 
    for index, edf_filename in enumerate(edf_filename_array):
        # Check if the file name is info_xx_xx.json
        if (json_filename.endswith('.json')):
            data_file = path_dataset + '/' + f['raw_name']
            if (edf_name_from_json == edf_filename):
                raw = mne.io.read_raw(data_file) # raw = raw format
                raw_array = raw.get_data() # raw_array = ndarray format
                print(raw_array[0].shape)

                # Concat ( New Code )
                for i in range(len(ch_names)): 
                    exec(f"main_array_channel_{i} = np.append(main_array_channel_{i}, raw_array{[i]})") 
                # Should be increasing
                print(main_array_channel_22.shape)
        else: 
            print(f'-------------  No {edf_name_from_json} in dataset folder -------------')
            continue

# Copy into bigger array
# main_all_concat = np.zeros([len(ch_names), main_array_channel_0.shape[0]])
# for i in range(len(ch_names)): 
#     exec(f"main_all_concat{[i]} = main_array_channel_{i}")  

print('--------Stop--------')

# Debugging line
# print(f'The main_all_concat variable shape is {main_all_concat.shape}')
# print(f'The main_all_concat variable dimension is {main_all_concat.ndim}')
# print(f'The main_all_concat variable dimension is {main_all_concat}')

for i in range(len(ch_names)):
    exec(f"np.save('chn{i}-{patient_chb}.npy', main_array_channel_{i})")