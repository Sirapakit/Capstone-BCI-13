import mne
import mne.viz
import numpy as np
import json
from scipy import signal
from scipy.stats import mode
import os

# Change Path for each patient
path = '../json_convert_to_npy/chb10'
patient_chb = 'chb10'
json_filename_array = os.listdir(path)
json_filename_array.sort()
sampling_rate = 256

# Get chn first
# 23 Channels
ch_names = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8-0', 'P8-O2', 'FZ-CZ', 'CZ-PZ', 'P7-T7', 'T7-FT9', 'FT9-FT10', 'FT10-T8', 'T8-P8-1']
# 28 Channels
# ch_names = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', '--0', 'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1', '--1', 'FZ-CZ', 'CZ-PZ', '--2', 'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', '--3', 'FP2-F8', 'F8-T8', 'T8-P8-0', 'P8-O2', '--4', 'P7-T7', 'T7-FT9', 'FT9-FT10', 'FT10-T8', 'T8-P8-1']

print(f'Channels name are {ch_names}')
print(f'There are {len(ch_names)} channels')
print(f'First channel is {ch_names[0]}')

print('--------Start--------')
for index, json_filename in enumerate(json_filename_array):
    # print(f'Investigating JSON: {json_filename}')

    # Open json data
    data = open('../' + 'json_convert_to_npy/' + patient_chb + '/' + json_filename)
    f = json.load(data)

    # get edf filename from json info
    edf_name_from_json = json_filename.split("_")[1] + '_' + json_filename.split("_")[2].split('.')[0] + '.edf'
    # print(f'Investigating EDF: {edf_name_from_json}')

    # Open dataset and create array name of edf files
    path_dataset = '../dataset/' + f['patient_ID']
    edf_filename_array = os.listdir(path_dataset)
    edf_filename_array.sort()

    # Create empty array varialbe for concat file
    for i in range(len(ch_names)): 
        exec(f"main_array_channel_{i} = np.array([])") 
        
# Looping through every files in json_info/chbxx/info_xx_xx.json
for index, json_filename in enumerate(json_filename_array):
    print(f'Investigating JSON: {json_filename}')

    # Read JSON data
    data = open('../' + 'json_convert_to_npy/' + patient_chb + '/' + json_filename)
    f = json.load(data)

    # Get edf filename from json info
    edf_name_from_json = json_filename.split("_")[1] + '_' + json_filename.split("_")[2].split('.')[0] + '.edf'
    print(f'Investigating EDF: {edf_name_from_json}')

    # Open dataset and create array name of edf files
    path_dataset = '../dataset/' + f['patient_ID']
    edf_filename_array = os.listdir(path_dataset)
    edf_filename_array.sort()

    # Rejected Files
#     rejected_files = [
# "chb20_01.edf",
# "chb20_02.edf",
# "chb20_03.edf",
# "chb20_04.edf",
# "chb20_05.edf",
# "chb20_06.edf"
# ]

    # Looping through every files in dataset/chbxx/chbxx_xx.edf 
    for index, edf_filename in enumerate(edf_filename_array):
        # Check if the file name is info_xx_xx.json
        if (json_filename.endswith('.json')):
            data_file = path_dataset + '/' + f['raw_name']
            if (edf_name_from_json == edf_filename):
                # if (edf_filename not in rejected_files):
                #     break
                raw = mne.io.read_raw(data_file) # raw = raw format
                raw_array = raw.get_data() # raw_array = ndarray format
                print(raw_array[0].shape)

                # Concat ( New Code )
                for i in range(len(ch_names)):
                    exec(f"main_array_channel_{i} = np.append(main_array_channel_{i}, raw_array{[i]})") 
                # Should be increasing
                print(main_array_channel_0.shape)
        else: 
            print(f'-------------  No {edf_name_from_json} in dataset folder -------------')
            continue
    else:
        continue

# Copy into bigger array
main_all_concat = np.zeros([len(ch_names), main_array_channel_0.shape[0]])
for i in range(len(ch_names)): 
    # exec(f"main_array_channel_{i} = (main_array_channel_{i}-np.min(main_array_channel_{i}))/(np.max(main_array_channel_{i})-np.min(main_array_channel_{i}))")
    exec(f"main_all_concat{[i]} = main_array_channel_{i}")  

# Delete variable for faster runtime
del main_array_channel_0, main_array_channel_1, main_array_channel_2, main_array_channel_3, main_array_channel_4
del main_array_channel_5, main_array_channel_6, main_array_channel_7, main_array_channel_8, main_array_channel_9
del main_array_channel_10, main_array_channel_11, main_array_channel_12, main_array_channel_13, main_array_channel_14
del main_array_channel_15, main_array_channel_16, main_array_channel_17, main_array_channel_18, main_array_channel_19
del main_array_channel_20, main_array_channel_21, main_array_channel_22
print('--------Stop--------')

# Debugging line
print(f'The main_all_concat variable shape is {main_all_concat.shape}')
# print(f'The main_all_concat variable dimension is {main_all_concat.ndim}')
# print(f'The main_all_concat variable dimension is {main_all_concat}')

#-----------------------------------------------------------------------------------------------------------#
# chb01
# seizure_start_info = np.array([10196, 12267, 52132, 55015, 62920, 71390, 90925]) * sampling_rate
# seizure_stop_info  = np.array([10236, 12294, 52172, 55066, 63010, 71483, 91026]) * sampling_rate

# chb02
# seizure_start_info = np.array([54130, 57931, 69128]) * sampling_rate
# seizure_stop_info  = np.array([54212, 58012, 69137]) * sampling_rate 

# chb03
# seizure_start_info = np.array([362, 4331, 7632, 9794, 120788, 124998, 127731]) * sampling_rate
# seizure_stop_info  = np.array([414, 4396, 7701, 9846, 120835, 125062, 127784]) * sampling_rate 

# chb04
# seizure_start_info = np.array([65402, 95476, 350451, 352554]) * sampling_rate
# seizure_stop_info  = np.array([65451, 95587, 350553, 352670]) * sampling_rate 

# chb05
# seizure_start_info = np.array([18427, 44296, 56327, 60061, 77958]) * sampling_rate
# seizure_stop_info  = np.array([18542, 44406, 56423, 60181, 78075]) * sampling_rate

# # chb06 
# seizure_start_info = np.array([1724, 21888, 42352, 43554, 49438, 126588, 139321, 157794, 225717, 235233]) * sampling_rate
# seizure_stop_info  = np.array([1738, 21903, 42367, 43574, 49458, 126604, 139333, 157807, 225729, 235249]) * sampling_rate

# chb07
# seizure_start_info = np.array([144081, 156846, 240635]) * sampling_rate
# seizure_stop_info  = np.array([144167, 156942, 240778]) * sampling_rate 

# chb08
# seizure_start_info = np.array([2670, 13656, 20988, 27617, 56083]) * sampling_rate
# seizure_stop_info  = np.array([2841, 13846, 21122, 27777, 56347]) * sampling_rate 

# chb09
# seizure_start_info = np.array([77868, 97387, 103632, 243937]) * sampling_rate
# seizure_stop_info  = np.array([77932, 97466, 103703, 243999]) * sampling_rate 

# chb10
seizure_start_info = np.array([63938, 122113, 139219, 154276, 162269, 170307, 174272]) * sampling_rate
seizure_stop_info  = np.array([63973, 122183, 139284, 154334, 162345, 170396, 174326]) * sampling_rate

# chb11
# seizure_start_info = np.array([111898, 117895, 120254]) * sampling_rate
# seizure_stop_info  = np.array([111920, 117927, 121006]) * sampling_rate 

# chb12
# Part 1
# seizure_start_info = np.array([1665, 3415, 5032, 5197, 5563, 6404, 10288, 10709, 11411, 11629, 15514, 27913, 28085, 28290]) * sampling_rate
# seizure_stop_info  = np.array([1726, 3447, 5045, 5220, 5583, 6430, 10320, 10741, 11443, 11674, 15551, 27993, 28182, 28330]) * sampling_rate 
# Part 2
# rejected_samples = 45684
# seizure_start_info = np.array([47845, 48087, 57113, 65224, 66474, 66642, 66822, 67040, 78775, 79021, 79246, 79752, 80289]) * sampling_rate - rejected_samples * sampling_rate
# seizure_stop_info  = np.array([47866, 48110, 57140, 65249, 66497, 66685, 66877, 67086, 78826, 79049, 79275, 79777, 80312]) * sampling_rate - rejected_samples * sampling_rate

# chb13
# Part 1
# rejected_samples = 57600
# seizure_start_info = np.array([59677, 62134]) * sampling_rate - rejected_samples * sampling_rate
# seizure_stop_info  = np.array([59721, 62204]) * sampling_rate - rejected_samples * sampling_rate
# Part 2
# rejected_samples = 97200
# seizure_start_info = np.array([97658, 99636, 106874, 111339, 112238, 116051, 116826, 117864]) * sampling_rate - rejected_samples * sampling_rate
# seizure_stop_info  = np.array([97678, 99650, 106891, 111401, 112260, 116116, 116891, 117921]) * sampling_rate - rejected_samples * sampling_rate

# chb14
# seizure_start_info = np.array([9186, 12172, 13617, 16311, 23438, 42839, 44239, 71233]) * sampling_rate
# seizure_stop_info  = np.array([9200, 12192, 13639, 16325, 23479, 42859, 44261, 71249]) * sampling_rate 

# chb15
# rejected_samples = 21602
# seizure_start_info = np.array([33484, 51993, 59527, 65409, 69162, 76478, 88153, 105236, 106780, 107764, 114924, 116310, 126780, 129874, 130454, 131135, 131790, 133039, 137562]) * sampling_rate - rejected_samples*sampling_rate
# seizure_stop_info  = np.array([33515, 52150, 59562, 65464, 69367, 76668, 88273, 105296, 106899, 107827, 115031, 116450, 126851, 129929, 130631, 131206, 131861, 133071, 137670]) * sampling_rate - rejected_samples*sampling_rate

# chb16
# Part 1 
# seizure_start_info = np.array([34690, 37120, 48654, 55214, 57827, 59294, 59762, 60890]) * sampling_rate
# seizure_stop_info  = np.array([34699, 37129, 48668, 55220, 57836, 59300, 59770, 60898]) * sampling_rate
# Part 2
# seizure_start_info = np.array([627, 1909]) * sampling_rate
# seizure_stop_info  = np.array([635, 1916]) * sampling_rate


# chb17
# seizure_start_info = np.array([2282, 6625, 35536]) * sampling_rate
# seizure_stop_info  = np.array([2372, 6740, 35624]) * sampling_rate

# chb18
# rejected_samples = 90011
# seizure_start_info = np.array([104288, 104952, 110098, 112193, 123281, 125148]) * sampling_rate - rejected_samples*sampling_rate
# seizure_stop_info  = np.array([104338, 104982, 110166, 112248, 123349, 125194]) * sampling_rate - rejected_samples*sampling_rate

# chb19
# rejected_samples 
# seizure_start_info = np.array([97499, 103776, 107571]) * sampling_rate
# seizure_stop_info  = np.array([97577, 103853, 107652]) * sampling_rate

# chb20
# seizure_start_info = np.array([32500, 37446, 38504, 41577, 43596, 44895, 49032, 98723]) * sampling_rate
# seizure_stop_info  = np.array([32529, 37476, 38543, 41615, 43631, 44944, 49067, 98762]) * sampling_rate

# chb21
# seizure_start_info = np.array([66087, 71026, 73392, 77542]) * sampling_rate
# seizure_stop_info  = np.array([66143, 71076, 73473, 77554]) * sampling_rate

# chb22
# seizure_start_info = np.array([60978, 78750, 98474]) * sampling_rate
# seizure_stop_info  = np.array([61036, 78824, 98546]) * sampling_rate

# chb23
# seizure_start_info = np.array([3962, 10371, 15150, 22977, 27273, 28893, 29968]) * sampling_rate
# seizure_stop_info  = np.array([4075, 10391, 15197, 23048, 27335, 28920, 30052]) * sampling_rate

# for add seizure event + label
main_seizure_only = np.array([])
main_event_only = np.array([])

###########################################
# Interictal: 0, Preictal:1, Ictal: 2     #
# Manual #
# 2 Cases ( 1. Enough gap ( > 3hrs ) 2. Not Enough ( 1. < 1 hr  2. < 3 hrs ( same code ))) #

# Seizure 0 ( More ) 
seizure_period_0 = main_all_concat[:,seizure_start_info[0]-10800*sampling_rate: seizure_stop_info[0]]
event_period_0   = np.zeros([1, seizure_period_0.shape[1]])
event_period_0[0][-((3600+35) * sampling_rate): -(35 * sampling_rate + 1)] = 1
event_period_0[0][-(35 * sampling_rate):] = 2
print(f'{(seizure_period_0.shape)} = {(event_period_0.shape)}')
print(f'Count 0 in event_period_0: {np.count_nonzero(event_period_0==0)}')
print(f'Count 1 in event_period_0: {np.count_nonzero(event_period_0==1)}')
print(f'Count 2 in event_period_0: {np.count_nonzero(event_period_0==2)}')
print("-----------------------------------------------------------------")

# Seizure 1 ( More ) 
seizure_period_1 = main_all_concat[:, seizure_start_info[1]-10800*sampling_rate: seizure_stop_info[1]]
event_period_1   = np.zeros([1, seizure_period_1.shape[1]])
event_period_1[0][-((3600+70) * sampling_rate): -(70 * sampling_rate + 1)] = 1
event_period_1[0][-(70 * sampling_rate):] = 2
print(f'Count 0 in event_period_1: {np.count_nonzero(event_period_1==0)}')
print(f'Count 1 in event_period_1: {np.count_nonzero(event_period_1==1)}')
print(f'Count 2 in event_period_1: {np.count_nonzero(event_period_1==2)}')
print("-----------------------------------------------------------------")

# Seizure 2 ( More ) 
seizure_period_2 = main_all_concat[:, seizure_start_info[2]-10800*sampling_rate: seizure_stop_info[2]]
event_period_2   = np.zeros([1, seizure_period_2.shape[1]])
event_period_2[0][-((3600+65) * sampling_rate): -(65 * sampling_rate + 1)] = 1
event_period_2[0][-(65 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_2==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_2==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_2==2)}')
print("-----------------------------------------------------------------")

# Seizure 3 ( More ) 
seizure_period_3 = main_all_concat[:, seizure_start_info[3]-10800*sampling_rate: seizure_stop_info[3]]
event_period_3   = np.zeros([1, seizure_period_3.shape[1]])
event_period_3[0][-((3600+58) * sampling_rate): -(58 * sampling_rate + 1)] = 1
event_period_3[0][-(58 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_3==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_3==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_3==2)}')
print("-----------------------------------------------------------------")

# Seizure 4 ( Less ) 
seizure_period_4 = main_all_concat[:, seizure_stop_info[3]: seizure_stop_info[4]]
event_period_4   = np.zeros([1, seizure_period_4.shape[1]])
event_period_4[0][-((3600+76) * sampling_rate): -(76 * sampling_rate + 1)] = 1
event_period_4[0][-(76 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_4==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_4==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_4==2)}')
print("-----------------------------------------------------------------")

# Seizure 5 ( Less ) 
seizure_period_5 = main_all_concat[:, seizure_stop_info[4]: seizure_stop_info[5]]
event_period_5   = np.zeros([1, seizure_period_5.shape[1]])
event_period_5[0][-((3600+89) * sampling_rate): -(89 * sampling_rate + 1)] = 1
event_period_5[0][-(89 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_5==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_5==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_5==2)}')
print("-----------------------------------------------------------------")

# Seizure 6 ( Less ) 
seizure_period_6 = main_all_concat[:, seizure_stop_info[5]: seizure_stop_info[6]]
event_period_6   = np.zeros([1, seizure_period_6.shape[1]])
event_period_6[0][-((3600+54) * sampling_rate): -(54 * sampling_rate + 1)] = 1
event_period_6[0][-(54 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_6==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_6==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_6==2)}')
print("-----------------------------------------------------------------")

# # Seizure 7 ( More ) 
# seizure_period_7 = main_all_concat[:, seizure_start_info[6] - 10800*sampling_rate: seizure_stop_info[7]]
# event_period_7   = np.zeros([1, seizure_period_7.shape[1]])
# event_period_7[0][-((3600+39) * sampling_rate): -(39 * sampling_rate + 1)] = 1
# event_period_7[0][-(39 * sampling_rate):] = 2
# print(f'Count 0 in event_period_7: {np.count_nonzero(event_period_7==0)}')
# print(f'Count 1 in event_period_7: {np.count_nonzero(event_period_7==1)}')
# print(f'Count 2 in event_period_7: {np.count_nonzero(event_period_7==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 8 ( More ) 
# seizure_period_8 = main_all_concat[:, seizure_start_info[7]: seizure_stop_info[8]]
# event_period_8   = np.zeros([1, seizure_period_8.shape[1]])
# event_period_8[0][: -(57 * sampling_rate + 1)] = 1
# event_period_8[0][-(57 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_8==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_8==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_8==2)}')
# print("-----------------------------------------------------------------")

# # # Seizure 9 ( Less ) 
# seizure_period_9 = main_all_concat[:, seizure_stop_info[8]: seizure_stop_info[9]]
# event_period_9   = np.zeros([1, seizure_period_9.shape[1]])
# event_period_9[0][: -(28 * sampling_rate + 1)] = 1
# event_period_9[0][-(28 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_9==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_9==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_9==2)}')
# print("-----------------------------------------------------------------")

# # # Seizure 10 ( Less ) 
# seizure_period_10 = main_all_concat[:, seizure_stop_info[9]: seizure_stop_info[10]]
# event_period_10   = np.zeros([1, seizure_period_10.shape[1]])
# event_period_10[0][: -(29 * sampling_rate + 1)] = 1
# event_period_10[0][-(29 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_10==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_10==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_10==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 11 ( Less ) 
# seizure_period_11 = main_all_concat[:, seizure_stop_info[10]: seizure_stop_info[11]]
# event_period_11   = np.zeros([1, seizure_period_11.shape[1]])
# event_period_11[0][: -(25 * sampling_rate + 1)] = 1
# event_period_11[0][-(25 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_11==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_11==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_11==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 12 ( More ) 
# seizure_period_12 = main_all_concat[:, seizure_stop_info[11] : seizure_stop_info[12]]
# event_period_12   = np.zeros([1, seizure_period_12.shape[1]])
# event_period_12[0][: -(23 * sampling_rate + 1)] = 1
# event_period_12[0][-(23 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_12==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_12==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_12==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 13 ( Less ) 
# seizure_period_13 = main_all_concat[:, seizure_stop_info[12]: seizure_stop_info[13]]
# event_period_13   = np.zeros([1, seizure_period_13.shape[1]])
# event_period_13[0][: -(40 * sampling_rate + 1)] = 1
# event_period_13[0][-(40 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_13==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_13==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_13==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 14 ( Less ) 
# seizure_period_14 = main_all_concat[:, seizure_stop_info[13]: seizure_stop_info[14]]
# event_period_14   = np.zeros([1, seizure_period_14.shape[1]])
# event_period_14[0][: -(177 * sampling_rate + 1)] = 1
# event_period_14[0][-(177 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_14==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_14==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_14==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 15 ( Less ) 
# seizure_period_15 = main_all_concat[:, seizure_stop_info[14]: seizure_stop_info[15]]
# event_period_15   = np.zeros([1, seizure_period_15.shape[1]])
# event_period_15[0][: -(71 * sampling_rate + 1)] = 1
# event_period_15[0][-(71 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_15==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_15==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_15==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 16 ( Less ) 
# seizure_period_16 = main_all_concat[:, seizure_stop_info[15]: seizure_stop_info[16]]
# event_period_16   = np.zeros([1, seizure_period_16.shape[1]])
# event_period_16[0][: -(71 * sampling_rate + 1)] = 1
# event_period_16[0][-(71 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_16==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_16==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_16==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 17 ( Less ) 
# seizure_period_17 = main_all_concat[:, seizure_stop_info[16]: seizure_stop_info[17]]
# event_period_17   = np.zeros([1, seizure_period_17.shape[1]])
# event_period_17[0][: -(32 * sampling_rate + 1)] = 1
# event_period_17[0][-(32 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_17==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_17==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_17==2)}')
# print("-----------------------------------------------------------------")

# # Seizure 18 ( Less ) 
# seizure_period_18 = main_all_concat[:, seizure_stop_info[17]: seizure_stop_info[18]]
# event_period_18   = np.zeros([1, seizure_period_18.shape[1]])
# event_period_18[0][-((3600+108) * sampling_rate): -(108 * sampling_rate + 1)] = 1
# event_period_18[0][-(108 * sampling_rate):] = 2
# print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_18==0)}')
# print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_18==1)}')
# print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_18==2)}')
# print("-----------------------------------------------------------------")


#-------------------------------------------------------------------------------------------------------------#
# Stack seizure with event
main_seizure_only = np.hstack((seizure_period_0, seizure_period_1, seizure_period_2, seizure_period_3, seizure_period_4, seizure_period_5, seizure_period_6))
main_event_only  = np.hstack((event_period_0, event_period_1, event_period_2, event_period_3, event_period_4, event_period_5, event_period_6))
data_with_event = np.vstack((main_seizure_only, main_event_only))
# Debugging line
print(f'Count 2: {np.count_nonzero(data_with_event[-1]==2)}')
print(f'data array stacked shape is: {data_with_event.shape}')
# Delete variable
del main_all_concat, main_seizure_only
print("--------Done Stacking Array--------")

# Filterbank V2
filter_band_1 = [-0.00107993806311353, -0.00106217163565181, -0.00104510238307734, -0.00102882032057693, -0.00101357133327608, -0.000999782376564196, -0.000988081923526628, -0.000979314791103734, -0.000974550588472947, -0.000975085164257233, -0.000982434580981359, -0.000998321312744441, -0.00102465254197012, -0.00106349061961468, -0.00111701594637719, -0.00118748272610121, -0.00127716823242759, -0.00138831641158684, -0.00152307681382854, -0.00168343999936680, -0.00187117069813066, -0.00208774011264687, -0.00233425883707135, -0.00261141192023950, -0.00291939762469068, -0.00325787142560709, -0.00362589675279992, -0.00402190390525106, -0.00444365846192655, -0.00488824037594689, -0.00535203477371457, -0.00583073528887907, -0.00631936054626844, -0.00681228417687241, -0.00730327849582716, -0.00778557171571805, -0.00825191830227724, -0.00869468181380980, -0.00910592930464674, -0.00947753612181550, -0.00980129968806068, -0.0100690606482630, -0.0102728295648152, -0.0104049171848486, -0.0104580661720998, -0.0104255821018470, -0.0103014614612624, -0.0100805143815706, -0.00975847985367612, -0.00933213124576528, -0.00879937004933520, -0.00815930592792519, -0.00741232132849578, -0.00656011913616001, -0.00560575210535546, -0.00455363308044548, -0.00340952532147838, -0.00218051257124607, -0.000874948832308795, 0.000497611838562294, 0.00192650487206738, 0.00340006308460933, 0.00490574163233417, 0.00643025841693759, 0.00795974805938918, 0.00947992730667490, 0.0109762695191370, 0.0124341857062006, 0.0138392094397595, 0.0151771828800697, 0.0164344411006942, 0.0175979918980667, 0.0186556883179377, 0.0195963912248275, 0.0204101193802545, 0.0210881846787323, 0.0216233104143159, 0.0220097307110830, 0.0222432695439173, 0.0223213980962941, 0.0222432695439173, 0.0220097307110830, 0.0216233104143159, 0.0210881846787323, 0.0204101193802545, 0.0195963912248275, 0.0186556883179377, 0.0175979918980667, 0.0164344411006942, 0.0151771828800697, 0.0138392094397595, 0.0124341857062006, 0.0109762695191370, 0.00947992730667490, 0.00795974805938918, 0.00643025841693759, 0.00490574163233417, 0.00340006308460933, 0.00192650487206738, 0.000497611838562294, -0.000874948832308795, -0.00218051257124607, -0.00340952532147838, -0.00455363308044548, -0.00560575210535546, -0.00656011913616001, -0.00741232132849578, -0.00815930592792519, -0.00879937004933520, -0.00933213124576528, -0.00975847985367612, -0.0100805143815706, -0.0103014614612624, -0.0104255821018470, -0.0104580661720998, -0.0104049171848486, -0.0102728295648152, -0.0100690606482630, -0.00980129968806068, -0.00947753612181550, -0.00910592930464674, -0.00869468181380980, -0.00825191830227724, -0.00778557171571805, -0.00730327849582716, -0.00681228417687241, -0.00631936054626844, -0.00583073528887907, -0.00535203477371457, -0.00488824037594689, -0.00444365846192655, -0.00402190390525106, -0.00362589675279992, -0.00325787142560709, -0.00291939762469068, -0.00261141192023950, -0.00233425883707135, -0.00208774011264687, -0.00187117069813066, -0.00168343999936680, -0.00152307681382854, -0.00138831641158684, -0.00127716823242759, -0.00118748272610121, -0.00111701594637719, -0.00106349061961468, -0.00102465254197012, -0.000998321312744441, -0.000982434580981359, -0.000975085164257233, -0.000974550588472947, -0.000979314791103734, -0.000988081923526628, -0.000999782376564196, -0.00101357133327608, -0.00102882032057693, -0.00104510238307734, -0.00106217163565181, -0.00107993806311353]
filter_band_2 = [9.24465419620629e-05, 8.85624593951150e-05, 7.71308595935144e-05, 5.70667383037532e-05, 2.71502517337408e-05, -1.39162505258435e-05, -6.74125471153623e-05, -0.000134468936260427, -0.000215904519097345, -0.000312044134034648, -0.000422525279195401, -0.000546108402760712, -0.000680505294621459, -0.000822240854706973, -0.000966563160628693, -0.00110741547217309, -0.00123748160426776, -0.00134831303558421, -0.00143054230876264, -0.00147418287805954, -0.00146901076845603, -0.00140501845566192, -0.00127292650876755, -0.00106473401558667, -0.000774284890716866, -0.000397824087464417, 6.54842924164026e-05, 0.000613105802771138, 0.00123877964715837, 0.00193228420268682, 0.00267934707924663, 0.00346171805939925, 0.00425741741491116, 0.00504116525831228, 0.00578499001877723, 0.00645900613464317, 0.00703234296818263, 0.00747419913051841, 0.00775498921936623, 0.00784754377173012, 0.00772831834202055, 0.00737856431405794, 0.00678541256605374, 0.00594282158407318, 0.00485234413562198, 0.00352367115950149, 0.00197491800175350, 0.000232626344659053, -0.00166853513072734, -0.00368637747773276, -0.00577210017489262, -0.00787148447704744, -0.00992634244996560, -0.0118761816927611, -0.0136600358620998, -0.0152184027869560, -0.0164952255876270, -0.0174398481043267, -0.0180088743319081, -0.0181678625858013, -0.0178927888246527, -0.0171712198550594, -0.0160031458646953, -0.0144014325924475, -0.0123918660767997, -0.0100127768773624, -0.00731424542869993, -0.00435690520850040, -0.00121037511192789, 0.00204863374797808, 0.00533847919039576, 0.00857494895907577, 0.0116737453084885, 0.0145530114787414, 0.0171358158194882, 0.0193525098367172, 0.0211428800075092, 0.0224580197269964, 0.0232618569940669, 0.0235322850762632, 0.0232618569940669, 0.0224580197269964, 0.0211428800075092, 0.0193525098367172, 0.0171358158194882, 0.0145530114787414, 0.0116737453084885, 0.00857494895907577, 0.00533847919039576, 0.00204863374797808, -0.00121037511192789, -0.00435690520850040, -0.00731424542869993, -0.0100127768773624, -0.0123918660767997, -0.0144014325924475, -0.0160031458646953, -0.0171712198550594, -0.0178927888246527, -0.0181678625858013, -0.0180088743319081, -0.0174398481043267, -0.0164952255876270, -0.0152184027869560, -0.0136600358620998, -0.0118761816927611, -0.00992634244996560, -0.00787148447704744, -0.00577210017489262, -0.00368637747773276, -0.00166853513072734, 0.000232626344659053, 0.00197491800175350, 0.00352367115950149, 0.00485234413562198, 0.00594282158407318, 0.00678541256605374, 0.00737856431405794, 0.00772831834202055, 0.00784754377173012, 0.00775498921936623, 0.00747419913051841, 0.00703234296818263, 0.00645900613464317, 0.00578499001877723, 0.00504116525831228, 0.00425741741491116, 0.00346171805939925, 0.00267934707924663, 0.00193228420268682, 0.00123877964715837, 0.000613105802771138, 6.54842924164026e-05, -0.000397824087464417, -0.000774284890716866, -0.00106473401558667, -0.00127292650876755, -0.00140501845566192, -0.00146901076845603, -0.00147418287805954, -0.00143054230876264, -0.00134831303558421, -0.00123748160426776, -0.00110741547217309, -0.000966563160628693, -0.000822240854706973, -0.000680505294621459, -0.000546108402760712, -0.000422525279195401, -0.000312044134034648, -0.000215904519097345, -0.000134468936260427, -6.74125471153623e-05, -1.39162505258435e-05, 2.71502517337408e-05, 5.70667383037532e-05, 7.71308595935144e-05, 8.85624593951150e-05, 9.24465419620629e-05]
filter_band_3 = [4.05568493008054e-05, 9.91986524849151e-06, -3.27975086399816e-05, -8.71016238998287e-05, -0.000151741668989157, -0.000224489182257267, -0.000301913530300002, -0.000379201424793642, -0.000450073733756132, -0.000506851157361419, -0.000540711226656778, -0.000542162798717908, -0.000501741854739701, -0.000410905830235914, -0.000263075432219409, -5.47458685338766e-05, 0.000213433270226274, 0.000535725619110375, 0.000900644858523925, 0.00129067647326527, 0.00168248182066925, 0.00204765148890000, 0.00235403403202537, 0.00256761743757390, 0.00265488777315244, 0.00258553676214860, 0.00233534233655093, 0.00188900828070861, 0.00124272525120117, 0.000406209220132064, -0.000596012995581380, -0.00172426723714936, -0.00292448677191714, -0.00413012967795762, -0.00526524662184444, -0.00624859622756019, -0.00699861435378107, -0.00743895964455144, -0.00750428789865896, -0.00714585870746563, -0.00633655484898834, -0.00507490181869828, -0.00338771325912798, -0.00133105721554970, 0.00101066503160708, 0.00352761676354430, 0.00608935564848193, 0.00855141143390244, 0.0107632919785987, 0.0125774771087851, 0.0138588628202628, 0.0144940537772940, 0.0143998762693351, 0.0135305006296050, 0.0118826225076365, 0.00949825410605768, 0.00646481423313198, 0.00291237165883950, -0.000991920666205665, -0.00505197457435432, -0.00905309209194124, -0.0127739002519791, -0.0159992002606525, -0.0185329502142794, -0.0202105643226907, -0.0209097288723878, -0.0205590063253225, -0.0191436206109062, -0.0167079818441980, -0.0133547072228570, -0.00924011402047021, -0.00456638602385302, 0.000429168621809851, 0.00548715712157735, 0.0103406720601879, 0.0147305161998462, 0.0184201539030476, 0.0212094683046178, 0.0229464705649707, 0.0235362306803060, 0.0229464705649707, 0.0212094683046178, 0.0184201539030476, 0.0147305161998462, 0.0103406720601879, 0.00548715712157735, 0.000429168621809851, -0.00456638602385302, -0.00924011402047021, -0.0133547072228570, -0.0167079818441980, -0.0191436206109062, -0.0205590063253225, -0.0209097288723878, -0.0202105643226907, -0.0185329502142794, -0.0159992002606525, -0.0127739002519791, -0.00905309209194124, -0.00505197457435432, -0.000991920666205665, 0.00291237165883950, 0.00646481423313198, 0.00949825410605768, 0.0118826225076365, 0.0135305006296050, 0.0143998762693351, 0.0144940537772940, 0.0138588628202628, 0.0125774771087851, 0.0107632919785987, 0.00855141143390244, 0.00608935564848193, 0.00352761676354430, 0.00101066503160708, -0.00133105721554970, -0.00338771325912798, -0.00507490181869828, -0.00633655484898834, -0.00714585870746563, -0.00750428789865896, -0.00743895964455144, -0.00699861435378107, -0.00624859622756019, -0.00526524662184444, -0.00413012967795762, -0.00292448677191714, -0.00172426723714936, -0.000596012995581380, 0.000406209220132064, 0.00124272525120117, 0.00188900828070861, 0.00233534233655093, 0.00258553676214860, 0.00265488777315244, 0.00256761743757390, 0.00235403403202537, 0.00204765148890000, 0.00168248182066925, 0.00129067647326527, 0.000900644858523925, 0.000535725619110375, 0.000213433270226274, -5.47458685338766e-05, -0.000263075432219409, -0.000410905830235914, -0.000501741854739701, -0.000542162798717908, -0.000540711226656778, -0.000506851157361419, -0.000450073733756132, -0.000379201424793642, -0.000301913530300002, -0.000224489182257267, -0.000151741668989157, -8.71016238998287e-05, -3.27975086399816e-05, 9.91986524849151e-06, 4.05568493008054e-05]
filter_band_4 = [-2.37755465563127e-05, -7.54488501182026e-05, -0.000135185097965791, -0.000197126149209651, -0.000253782016444110, -0.000296286963540858, -0.000314923213857793, -0.000299982284046228, -0.000242979151143352, -0.000138157166280288, 1.58659742249548e-05, 0.000214542651262042, 0.000446219889609860, 0.000691652560156669, 0.000924481350377313, 0.00111286377973549, 0.00122230759916255, 0.00121957954199551, 0.00107737044646575, 0.000779217889097063, 0.000324049487221106, -0.000270358346199424, -0.000965689060838149, -0.00170372124543236, -0.00240962752828757, -0.00299797065631739, -0.00338107660121645, -0.00347910245385377, -0.00323079449792006, -0.00260369755704932, -0.00160247252035717, -0.000274034247236334, 0.00129155165471530, 0.00296508703465547, 0.00458733079453202, 0.00598272046271484, 0.00697667859854179, 0.00741491155904696, 0.00718269865888140, 0.00622195922379128, 0.00454391759190356, 0.00223547980767094, -0.000542021708534469, -0.00356231128067265, -0.00655159486739934, -0.00921271813784052, -0.0112539905877847, -0.0124199187102494, -0.0125206622281902, -0.0114569269737111, -0.00923727000300756, -0.00598541088701646, -0.00193607019803594, 0.00258099389695042, 0.00716782362824101, 0.0113938187888937, 0.0148367965221444, 0.0171255697855808, 0.0179796867114379, 0.0172420530405899, 0.0149007056614412, 0.0110969776463657, 0.00611860559634064, 0.000377849191640076, -0.00562373664152806, -0.0113407830238971, -0.0162355725646101, -0.0198304580313102, -0.0217559498425204, -0.0217894840688195, -0.0198807109428206, -0.0161604287726853, -0.0109319027790520, -0.00464508759955234, 0.00214396994780568, 0.00882472155742775, 0.0147897009010188, 0.0194924290519816, 0.0224998814893366, 0.0235342620603006, 0.0224998814893366, 0.0194924290519816, 0.0147897009010188, 0.00882472155742775, 0.00214396994780568, -0.00464508759955234, -0.0109319027790520, -0.0161604287726853, -0.0198807109428206, -0.0217894840688195, -0.0217559498425204, -0.0198304580313102, -0.0162355725646101, -0.0113407830238971, -0.00562373664152806, 0.000377849191640076, 0.00611860559634064, 0.0110969776463657, 0.0149007056614412, 0.0172420530405899, 0.0179796867114379, 0.0171255697855808, 0.0148367965221444, 0.0113938187888937, 0.00716782362824101, 0.00258099389695042, -0.00193607019803594, -0.00598541088701646, -0.00923727000300756, -0.0114569269737111, -0.0125206622281902, -0.0124199187102494, -0.0112539905877847, -0.00921271813784052, -0.00655159486739934, -0.00356231128067265, -0.000542021708534469, 0.00223547980767094, 0.00454391759190356, 0.00622195922379128, 0.00718269865888140, 0.00741491155904696, 0.00697667859854179, 0.00598272046271484, 0.00458733079453202, 0.00296508703465547, 0.00129155165471530, -0.000274034247236334, -0.00160247252035717, -0.00260369755704932, -0.00323079449792006, -0.00347910245385377, -0.00338107660121645, -0.00299797065631739, -0.00240962752828757, -0.00170372124543236, -0.000965689060838149, -0.000270358346199424, 0.000324049487221106, 0.000779217889097063, 0.00107737044646575, 0.00121957954199551, 0.00122230759916255, 0.00111286377973549, 0.000924481350377313, 0.000691652560156669, 0.000446219889609860, 0.000214542651262042, 1.58659742249548e-05, -0.000138157166280288, -0.000242979151143352, -0.000299982284046228, -0.000314923213857793, -0.000296286963540858, -0.000253782016444110, -0.000197126149209651, -0.000135185097965791, -7.54488501182026e-05, -2.37755465563127e-05]
filter_band_5 = [-8.25409658428109e-05, -0.000139765758160562, -0.000189984479364148, -0.000220977960242162, -0.000220793193805340, -0.000179687654761451, -9.23670535970729e-05, 3.97530713518094e-05, 0.000206703148531369, 0.000389091642483222, 0.000558776442653258, 0.000681488108663034, 0.000721504882577139, 0.000648039691338143, 0.000442509436653692, 0.000105423927229312, -0.000338627172940407, -0.000839395554312734, -0.00132396245541680, -0.00170477966840913, -0.00189232994728499, -0.00181095513780384, -0.00141547710442119, -0.000705615253438141, 0.000264936464691418, 0.00138746198484246, 0.00250684960173142, 0.00344000711841334, 0.00400238630718909, 0.00403918325420695, 0.00345640445847324, 0.00224629919034312, 0.000501876446252219, -0.00158357268836834, -0.00373393519175673, -0.00562399723501012, -0.00692579126630320, -0.00736131332303243, -0.00675352415258184, -0.00506691465401633, -0.00242971663116624, 0.000867920242794556, 0.00440203120341257, 0.00766731556102946, 0.0101478673294528, 0.0113964505623437, 0.0111103322505341, 0.00919119953064077, 0.00577822238111578, 0.00124677915207280, -0.00382968985574208, -0.00875150691469671, -0.0127894463078470, -0.0152928959345073, -0.0157933756007119, -0.0140869905935770, -0.0102817048118563, -0.00480001198900324, 0.00166595956073591, 0.00824259971935006, 0.0139949535886911, 0.0180620435282273, 0.0197874371423750, 0.0188249723290754, 0.0152025384562556, 0.00933258862069921, 0.00196581290867215, -0.00590701624719734, -0.0131919301907557, -0.0188479793505628, -0.0220398869611243, -0.0222641987415113, -0.0194294627261450, -0.0138775155764657, -0.00634160441110654, 0.00215346776410426, 0.0104351718247020, 0.0173502612331720, 0.0219304600697320, 0.0235323211560674, 0.0219304600697320, 0.0173502612331720, 0.0104351718247020, 0.00215346776410426, -0.00634160441110654, -0.0138775155764657, -0.0194294627261450, -0.0222641987415113, -0.0220398869611243, -0.0188479793505628, -0.0131919301907557, -0.00590701624719734, 0.00196581290867215, 0.00933258862069921, 0.0152025384562556, 0.0188249723290754, 0.0197874371423750, 0.0180620435282273, 0.0139949535886911, 0.00824259971935006, 0.00166595956073591, -0.00480001198900324, -0.0102817048118563, -0.0140869905935770, -0.0157933756007119, -0.0152928959345073, -0.0127894463078470, -0.00875150691469671, -0.00382968985574208, 0.00124677915207280, 0.00577822238111578, 0.00919119953064077, 0.0111103322505341, 0.0113964505623437, 0.0101478673294528, 0.00766731556102946, 0.00440203120341257, 0.000867920242794556, -0.00242971663116624, -0.00506691465401633, -0.00675352415258184, -0.00736131332303243, -0.00692579126630320, -0.00562399723501012, -0.00373393519175673, -0.00158357268836834, 0.000501876446252219, 0.00224629919034312, 0.00345640445847324, 0.00403918325420695, 0.00400238630718909, 0.00344000711841334, 0.00250684960173142, 0.00138746198484246, 0.000264936464691418, -0.000705615253438141, -0.00141547710442119, -0.00181095513780384, -0.00189232994728499, -0.00170477966840913, -0.00132396245541680, -0.000839395554312734, -0.000338627172940407, 0.000105423927229312, 0.000442509436653692, 0.000648039691338143, 0.000721504882577139, 0.000681488108663034, 0.000558776442653258, 0.000389091642483222, 0.000206703148531369, 3.97530713518094e-05, -9.23670535970729e-05, -0.000179687654761451, -0.000220793193805340, -0.000220977960242162, -0.000189984479364148, -0.000139765758160562, -8.25409658428109e-05]
filter_band_6 = [-0.000124474476447680, -0.000166430371954174, -0.000178974155619620, -0.000149042763266301, -7.07388253912474e-05, 5.14277545020950e-05, 0.000200664424675636, 0.000348301193138761, 0.000457221618568168, 0.000488545218222327, 0.000410942063553405, 0.000210957628724503, -9.81460042396853e-05, -0.000471929347894839, -0.000837243431727199, -0.00110295949835311, -0.00117834194097923, -0.000996150617200605, -0.000535510707673397, 0.000161560267975292, 0.000985797123590716, 0.00177239091013768, 0.00232923332486819, 0.00247795313779849, 0.00209992991682414, 0.00117668577243324, -0.000186482150451331, -0.00176253098238370, -0.00323437952045760, -0.00425360527967623, -0.00451634901092970, -0.00384089885275125, -0.00222866726819880, 0.000108391383032695, 0.00276522017992940, 0.00520810023208913, 0.00687737451376724, 0.00730959079597825, 0.00625330333071820, 0.00375115765833474, 0.000165526670111853, -0.00386455277493526, -0.00753293498897343, -0.0100247605696052, -0.0106931237243915, -0.00921630316037805, -0.00569866891630660, -0.000687680011240790, 0.00490423631975691, 0.00996384454046420, 0.0133983321434721, 0.0143697054220240, 0.0124922031425717, 0.00794707307463684, 0.00148400910633410, -0.00569869731276041, -0.0121772666044315, -0.0165871803017459, -0.0179121084507418, -0.0157154120538397, -0.0102617157875742, -0.00249705487140185, 0.00611502057380312, 0.0138732195774573, 0.0191799675457783, 0.0208749490662926, 0.0184901357751648, 0.0123698434559303, 0.00362610975855164, -0.00606635011816188, -0.0147972903893698, -0.0208050508273709, -0.0228389012679376, -0.0204237067876438, -0.0139700202389020, -0.00470413870125710, 0.00557000838130574, 0.0148299267850633, 0.0212415747581022, 0.0235306770377631, 0.0212415747581022, 0.0148299267850633, 0.00557000838130574, -0.00470413870125710, -0.0139700202389020, -0.0204237067876438, -0.0228389012679376, -0.0208050508273709, -0.0147972903893698, -0.00606635011816188, 0.00362610975855164, 0.0123698434559303, 0.0184901357751648, 0.0208749490662926, 0.0191799675457783, 0.0138732195774573, 0.00611502057380312, -0.00249705487140185, -0.0102617157875742, -0.0157154120538397, -0.0179121084507418, -0.0165871803017459, -0.0121772666044315, -0.00569869731276041, 0.00148400910633410, 0.00794707307463684, 0.0124922031425717, 0.0143697054220240, 0.0133983321434721, 0.00996384454046420, 0.00490423631975691, -0.000687680011240790, -0.00569866891630660, -0.00921630316037805, -0.0106931237243915, -0.0100247605696052, -0.00753293498897343, -0.00386455277493526, 0.000165526670111853, 0.00375115765833474, 0.00625330333071820, 0.00730959079597825, 0.00687737451376724, 0.00520810023208913, 0.00276522017992940, 0.000108391383032695, -0.00222866726819880, -0.00384089885275125, -0.00451634901092970, -0.00425360527967623, -0.00323437952045760, -0.00176253098238370, -0.000186482150451331, 0.00117668577243324, 0.00209992991682414, 0.00247795313779849, 0.00232923332486819, 0.00177239091013768, 0.000985797123590716, 0.000161560267975292, -0.000535510707673397, -0.000996150617200605, -0.00117834194097923, -0.00110295949835311, -0.000837243431727199, -0.000471929347894839, -9.81460042396853e-05, 0.000210957628724503, 0.000410942063553405, 0.000488545218222327, 0.000457221618568168, 0.000348301193138761, 0.000200664424675636, 5.14277545020950e-05, -7.07388253912474e-05, -0.000149042763266301, -0.000178974155619620, -0.000166430371954174, -0.000124474476447680]
filter_band_7 = [-0.000141770477587749, -0.000148882394942387, -0.000106442601714509, -1.26935034614006e-05, 0.000117206561888634, 0.000251471359520787, 0.000347129040769892, 0.000360602970992915, 0.000261784626704936, 4.81437903813073e-05, -0.000245887283971033, -0.000549054395936652, -0.000765975056140324, -0.000801881388971367, -0.000594408372083050, -0.000143396946695176, 0.000472191433785915, 0.00109956400085174, 0.00154353042149476, 0.00161988276294632, 0.00121790932632461, 0.000353122156566525, -0.000809605476415364, -0.00197654197685413, -0.00279155576390546, -0.00293600292777483, -0.00223605595622782, -0.000744212343652850, 0.00123583365398243, 0.00319878116402658, 0.00455863519162206, 0.00481449301270966, 0.00371635261526015, 0.00137928783392910, -0.00169701474288976, -0.00472288705192619, -0.00681419856725113, -0.00724251871949201, -0.00567092943332195, -0.00230233531911540, 0.00211496430962177, 0.00644273387009780, 0.00944093528368766, 0.0101171529319686, 0.00804007494386833, 0.00352072516632554, -0.00240485559699594, -0.00820508611947958, -0.0122465674464071, -0.0132515331107565, -0.0106913235625034, -0.00499658605800042, 0.00249084873425328, 0.00982982864219756, 0.0149846680886039, 0.0163912716611793, 0.0134265836629676, 0.00664122917047246, -0.00232516191207188, -0.0111400670759408, -0.0173902694705318, -0.0192480834001858, -0.0160060918578712, -0.00832353403039843, 0.00189766468742829, 0.0119877562118853, 0.0192154754749806, 0.0215365868965898, 0.0181770191232290, 0.00988277229955338, -0.00124265384437511, -0.0122791072820976, -0.0202679731092238, -0.0230172453348936, -0.0197112303771132, -0.0111530515290893, 0.000432415982451068, 0.0119863848063738, 0.0204369884052293, 0.0235293390830873, 0.0204369884052293, 0.0119863848063738, 0.000432415982451068, -0.0111530515290893, -0.0197112303771132, -0.0230172453348936, -0.0202679731092238, -0.0122791072820976, -0.00124265384437511, 0.00988277229955338, 0.0181770191232290, 0.0215365868965898, 0.0192154754749806, 0.0119877562118853, 0.00189766468742829, -0.00832353403039843, -0.0160060918578712, -0.0192480834001858, -0.0173902694705318, -0.0111400670759408, -0.00232516191207188, 0.00664122917047246, 0.0134265836629676, 0.0163912716611793, 0.0149846680886039, 0.00982982864219756, 0.00249084873425328, -0.00499658605800042, -0.0106913235625034, -0.0132515331107565, -0.0122465674464071, -0.00820508611947958, -0.00240485559699594, 0.00352072516632554, 0.00804007494386833, 0.0101171529319686, 0.00944093528368766, 0.00644273387009780, 0.00211496430962177, -0.00230233531911540, -0.00567092943332195, -0.00724251871949201, -0.00681419856725113, -0.00472288705192619, -0.00169701474288976, 0.00137928783392910, 0.00371635261526015, 0.00481449301270966, 0.00455863519162206, 0.00319878116402658, 0.00123583365398243, -0.000744212343652850, -0.00223605595622782, -0.00293600292777483, -0.00279155576390546, -0.00197654197685413, -0.000809605476415364, 0.000353122156566525, 0.00121790932632461, 0.00161988276294632, 0.00154353042149476, 0.00109956400085174, 0.000472191433785915, -0.000143396946695176, -0.000594408372083050, -0.000801881388971367, -0.000765975056140324, -0.000549054395936652, -0.000245887283971033, 4.81437903813073e-05, 0.000261784626704936, 0.000360602970992915, 0.000347129040769892, 0.000251471359520787, 0.000117206561888634, -1.26935034614006e-05, -0.000106442601714509, -0.000148882394942387, -0.000141770477587749]
filter_band_8 = [-0.000131322864090573, -9.20484477639667e-05, 2.53987176117459e-06, 0.000129362962056063, 0.000244258573091784, 0.000294491766100860, 0.000238176808357216, 6.50209818924689e-05, -0.000189617664796327, -0.000445382422134092, -0.000596801052950172, -0.000550068053188173, -0.000266145323304105, 0.000206623203161043, 0.000727745607654990, 0.00109784148159482, 0.00112618317279741, 0.000712625010374597, -8.75629846170505e-05, -0.00104802503527458, -0.00182346537849892, -0.00206349622160021, -0.00155431277492680, -0.000335070572717083, 0.00126473780186853, 0.00269847796601591, 0.00337790182435039, 0.00289885979680380, 0.00123481999673090, -0.00118565649466088, -0.00356855642245605, -0.00500315407758021, -0.00479656397596925, -0.00277511884184999, 0.000571055550161086, 0.00417970312967896, 0.00674174891536940, 0.00716558790383315, 0.00501894119687815, 0.000775145757985712, -0.00425463810620914, -0.00831454141217942, -0.00980977197375426, -0.00791843939349877, -0.00297843991139096, 0.00351971150907404, 0.00937046214642208, 0.0123982207581128, 0.0112594673375258, 0.00600791246813818, -0.00180769635953964, -0.00958774757630088, -0.0145463185727163, -0.0147088620016593, -0.00968536810141525, -0.000919371923544815, 0.00871338924047480, 0.0158513505739599, 0.0178263571791068, 0.0136598529736378, 0.00450386574974249, -0.00666232456342051, -0.0160071055151228, -0.0201724201412270, -0.0174879999424419, -0.00863205138902866, 0.00352088248940939, 0.0148402252652243, 0.0213579978406805, 0.0206735501895400, 0.0128422804437680, 0.000417512883259509, -0.0123901362507810, -0.0211565077500430, -0.0227900151478283, -0.0166336600767266, -0.00472603371148702, 0.00888166118006524, 0.0195211062091161, 0.0235283254258358, 0.0195211062091161, 0.00888166118006524, -0.00472603371148702, -0.0166336600767266, -0.0227900151478283, -0.0211565077500430, -0.0123901362507810, 0.000417512883259509, 0.0128422804437680, 0.0206735501895400, 0.0213579978406805, 0.0148402252652243, 0.00352088248940939, -0.00863205138902866, -0.0174879999424419, -0.0201724201412270, -0.0160071055151228, -0.00666232456342051, 0.00450386574974249, 0.0136598529736378, 0.0178263571791068, 0.0158513505739599, 0.00871338924047480, -0.000919371923544815, -0.00968536810141525, -0.0147088620016593, -0.0145463185727163, -0.00958774757630088, -0.00180769635953964, 0.00600791246813818, 0.0112594673375258, 0.0123982207581128, 0.00937046214642208, 0.00351971150907404, -0.00297843991139096, -0.00791843939349877, -0.00980977197375426, -0.00831454141217942, -0.00425463810620914, 0.000775145757985712, 0.00501894119687815, 0.00716558790383315, 0.00674174891536940, 0.00417970312967896, 0.000571055550161086, -0.00277511884184999, -0.00479656397596925, -0.00500315407758021, -0.00356855642245605, -0.00118565649466088, 0.00123481999673090, 0.00289885979680380, 0.00337790182435039, 0.00269847796601591, 0.00126473780186853, -0.000335070572717083, -0.00155431277492680, -0.00206349622160021, -0.00182346537849892, -0.00104802503527458, -8.75629846170505e-05, 0.000712625010374597, 0.00112618317279741, 0.00109784148159482, 0.000727745607654990, 0.000206623203161043, -0.000266145323304105, -0.000550068053188173, -0.000596801052950172, -0.000445382422134092, -0.000189617664796327, 6.50209818924689e-05, 0.000238176808357216, 0.000294491766100860, 0.000244258573091784, 0.000129362962056063, 2.53987176117459e-06, -9.20484477639667e-05, -0.000131322864090573]

# Create 8 bands per chn
num_bands = 8
# Crop to five channel
# Done 0,1,2,3---4,5,6,7---8,9,10,11---12,13,14,15---16,17,18,19---20,21,22
# chn_start = 0
# chn_end = 4
# data_with_event = data_with_event[chn_start: chn_end+1, :]

data_filtered_array = np.zeros(((len(ch_names))*num_bands+1, data_with_event.shape[1]))
# 17 because 23 - 17 = 6 chn 
# 18 because 23 - 18 = 5 chn at a time
# 19 because 23 - 19 = 4 chn at a time
# 20 ==> 23 - 20 = 3
# 23 - 11 = 12

# for i in range(0, 3):
for i in range(len(ch_names)):
    data_filtered_array[i*num_bands+0][:]  = signal.filtfilt(filter_band_1, 1, data_with_event[i])
    data_filtered_array[i*num_bands+1][:]  = signal.filtfilt(filter_band_2, 1, data_with_event[i])
    data_filtered_array[i*num_bands+2][:]  = signal.filtfilt(filter_band_3, 1, data_with_event[i])
    data_filtered_array[i*num_bands+3][:]  = signal.filtfilt(filter_band_4, 1, data_with_event[i])
    data_filtered_array[i*num_bands+4][:]  = signal.filtfilt(filter_band_5, 1, data_with_event[i])
    data_filtered_array[i*num_bands+5][:]  = signal.filtfilt(filter_band_6, 1, data_with_event[i])
    data_filtered_array[i*num_bands+6][:]  = signal.filtfilt(filter_band_7, 1, data_with_event[i])
    data_filtered_array[i*num_bands+7][:]  = signal.filtfilt(filter_band_8, 1, data_with_event[i])

    print(f'###############Convolute channel {i+1} done###############')
data_filtered_array[-1][:] = main_event_only

print(f'Count 2: {np.count_nonzero(data_filtered_array[-1]==2)}')
print("--------Done Convolving--------")

del filter_band_1, filter_band_2, filter_band_3, filter_band_4, filter_band_5, filter_band_6, filter_band_7, filter_band_8


# Calculate Energy perband
chn_include_event = len(ch_names)
# 11 because 23 - 11 = 12 chb at a time
# 17 because 23 - 17 = 6 chn at a time
# 18 because 23 - 18 = 5 chn at a time

shifted_sec = 4
energy_array = np.zeros((num_bands*chn_include_event+1, int(data_filtered_array.shape[1]/(sampling_rate*shifted_sec))))
for feat in range(num_bands * chn_include_event + 1):
    start, end = 0, 2048
    count = 0
    if (feat != num_bands * chn_include_event):  
        while (end <= data_with_event.shape[1]):
            new_sub_array = np.zeros((1, 2048))
            new_sub_array = data_filtered_array[feat][:][start: end]
            energy_one_band = np.sum(np.power(new_sub_array, 2))
            energy_array[feat][count] = energy_one_band
            start += 1024
            end += 1024
            count += 1
    else :
        while (end <= data_with_event.shape[1]):
            energy_array[feat][count] = mode(data_filtered_array[feat][:][start: end], axis=None)[0][0] 
            start += 1024
            end += 1024
            count += 1

# Norm except for event
for i in range(num_bands * chn_include_event):
    energy_array[i] = (energy_array[i]-np.min(energy_array[i]))/(np.max(energy_array[i])-np.min(energy_array[i]))

# for i in range(num_bands * chn_include_event):
#     data_filtered_array[i] = (data_filtered_array[i]-np.min(data_filtered_array[i]))/(np.max(data_filtered_array[i])-np.min(data_filtered_array[i]))

# --------------------Rejected Channel---------------------------------
# Reject Unused Channel ( Bands )
# print(f'Before rejected: {energy_array.shape}')
# rows_to_reject = np.concatenate((np.arange(32, 40), np.arange(72, 80), np.arange(96, 104), np.arange(136, 144), np.arange(176, 184)))
# rows_to_reject = np.concatenate((np.arange(32, 40), np.arange(72, 80), np.arange(96, 104), np.arange(136, 144), np.arange(176, 192)))

# rows_to_reject = np.concatenate((np.arange(32, 40), np.arange(72, 80), np.arange(96, 112), np.arange(144, 152), np.arange(184, 192)))
# energy_array = np.delete(energy_array, rows_to_reject, axis=0)
# print(f'After rejected: {energy_array.shape}')
# --------------------Rejected Channel---------------------------------

# Debugging line
print(f'Count 2: {np.count_nonzero(energy_array[-1]==2)}')
print("--------Done Calculating Energy--------")

# Save file take some times
print('-------May take long time to save, be patient---------')
# have (737, xxxxx)
filename = "8bands-chb10-new.npy"
np.save(filename, energy_array)