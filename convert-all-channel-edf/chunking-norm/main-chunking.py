import mne
import mne.viz
import numpy as np
from scipy.stats import mode
import os

path_edf_concat = '../8-bands-filtfilt/chb02'
patient_id = 'chb02'

sampling_rate = 256

# chb01
# seizure_start_info = np.array([10196, 12267, 52132, 55015, 62920, 71390, 90925]) * sampling_rate
# seizure_stop_info  = np.array([10236, 12294, 52172, 55066, 63010, 71483, 91026]) * sampling_rate

# chb02
seizure_start_info = np.array([54130, 57931, 69128]) * sampling_rate
seizure_stop_info  = np.array([54212, 58012, 69137]) * sampling_rate 

# for add seizure event + label
main_seizure_only = np.array([])
main_event_only = np.array([])

os.listdir(path_edf_concat).sort()
for filename in os.listdir(path_edf_concat):
    file_path = os.path.join(path_edf_concat, filename)

    main_all_concat = np.load(file_path)

    ###########################################
    # Interictal: 0, Preictal:1, Ictal: 2     #
    # Manual #
    # 2 Cases ( 1. Enough gap ( > 3hrs ) 2. Not Enough ( 1. < 1 hr  2. < 3 hrs ( same code ))) #

    # Seizure 0 ( More ) corr
    seizure_period_0 = main_all_concat[:, seizure_start_info[0]: seizure_stop_info[0]]
    event_period_0   = np.zeros([1, seizure_period_0.shape[1]])
    event_period_0[0][-((3600+82) * sampling_rate): -(82 * sampling_rate + 1)] = 1
    event_period_0[0][-(82 * sampling_rate):] = 2
    print(f'{(seizure_period_0.shape)} = {(event_period_0.shape)}')
    print(f'Count 0 in event_period_0: {np.count_nonzero(event_period_0==0)}')
    print(f'Count 1 in event_period_0: {np.count_nonzero(event_period_0==1)}')
    print(f'Count 2 in event_period_0: {np.count_nonzero(event_period_0==2)}')
    print("-----------------------------------------------------------------")

    # Seizure 1 ( Less**** ) 
    seizure_period_1 = main_all_concat[:, seizure_stop_info[0]: seizure_stop_info[1]]
    event_period_1   = np.zeros([1, seizure_period_1.shape[1]])
    event_period_1[0][-((3600+81) * sampling_rate): -(81 * sampling_rate + 1)] = 1
    event_period_1[0][-(81 * sampling_rate):] = 2
    print(f'Count 0 in event_period_1: {np.count_nonzero(event_period_1==0)}')
    print(f'Count 1 in event_period_1: {np.count_nonzero(event_period_1==1)}')
    print(f'Count 2 in event_period_1: {np.count_nonzero(event_period_1==2)}')
    print("-----------------------------------------------------------------")
    
    # Seizure 2 ( More ) Correct
    seizure_period_2 = main_all_concat[:, seizure_start_info[2] - 10800 * sampling_rate: seizure_stop_info[2]]
    event_period_2   = np.zeros([1, seizure_period_2.shape[1]])
    event_period_2[0][7200 * sampling_rate: 10800 * sampling_rate] = 1
    event_period_2[0][10800 * sampling_rate:] = 2
    print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_2==0)}')
    print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_2==1)}')
    print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_2==2)}')
    print("-----------------------------------------------------------------")

    #-------------------------------------------------------------------------------------------------------------#
    # Stack seizure with event
    main_seizure_only = np.hstack((seizure_period_0, seizure_period_1, seizure_period_2))
    main_event_only  = np.hstack((event_period_0, event_period_1, event_period_2))
    # data_with_event = np.vstack((main_seizure_only, main_event_only))

    # Debugging line
    # print(f'Count 2: {np.count_nonzero(data_with_event[-1]==2)}')
    # print(f'data array stacked shape is: {data_with_event.shape}')
    print(f'Count 2: {np.count_nonzero(main_event_only[-1]==2)}')
    print(f'data array stacked shape is: {main_event_only.shape}')

    filename_to_save = filename.split(".")[0] + '_8bands.npy'
    np.save('./' + patient_id + '/' + filename_to_save, main_seizure_only)
    # Delete variable
    del main_all_concat, main_seizure_only

print("--------Done Stacking Array--------")

