import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
from scipy.stats import mode

# CHB01 in numpy (4, 6, 7, 13)
## CHB03 in numpy (5, 12, 16, 17)
## CHB03 oversampling in numpy (1, 5, 7, 13)

# CHB05 in numpy (0, 4,  12, 18)
## CHB06 in numpy (9, 16, 17, 22)
## CHB06 oversampling in numpy (1, 7, 15, 20)


## Careful for 28 channel check for dummy in CHB-MIT website
## CHB17 in numpy (3, 6, 18, 21) 
## CHB17 oversampling in numpy (3, 6, 14, 21)
## CHB20 in numpy (2, 23, 24, 25)
## CHB20 oversampling in numpy (3, 5, 19, 21)



patient_chb = "chb20"
data_channel_1 = np.load('../convert-all-channel-edf/edf-concat/chb20/chn3-chb20.npy')
data_channel_2 = np.load('../convert-all-channel-edf/edf-concat/chb20/chn5-chb20.npy')
data_channel_3 = np.load('../convert-all-channel-edf/edf-concat/chb20/chn19-chb20.npy')
data_channel_4 = np.load('../convert-all-channel-edf/edf-concat/chb20/chn21-chb20.npy')
# print(data_channel_4)

main_all_concat = np.vstack((data_channel_1, data_channel_2, data_channel_3, data_channel_4))
del data_channel_1, data_channel_2, data_channel_3, data_channel_4
# print(main_all_concat[2])

sampling_rate = 256
window_len = 8
overlapping = 4

# chb01
# seizure_start_info = np.array([10196, 12267, 52132, 55015, 62920, 71390, 90925]) * sampling_rate
# seizure_stop_info  = np.array([10236, 12294, 52172, 55066, 63010, 71483, 91026]) * sampling_rate

# chb03
# seizure_start_info = np.array([362, 4331, 7632, 9794, 120788, 124998, 127731]) * sampling_rate
# seizure_stop_info  = np.array([414, 4396, 7701, 9846, 120835, 125062, 127784]) * sampling_rate 

# chb05
# seizure_start_info = np.array([18427, 44296, 56327, 60061, 77958]) * sampling_rate
# seizure_stop_info  = np.array([18542, 44406, 56423, 60181, 78075]) * sampling_rate

# chb06 
# seizure_start_info = np.array([1724, 21888, 42352, 43554, 49438, 126588, 139321, 157794, 225717, 235233]) * sampling_rate
# seizure_stop_info  = np.array([1738, 21903, 42367, 43574, 49458, 126604, 139333, 157807, 225729, 235249]) * sampling_rate

# chb17
# seizure_start_info = np.array([2282, 6625, 35536]) * sampling_rate
# seizure_stop_info  = np.array([2372, 6740, 35624]) * sampling_rate

# chb20
seizure_start_info = np.array([32500, 37446, 38504, 41577, 43596, 44895, 49032, 98723]) * sampling_rate
seizure_stop_info  = np.array([32529, 37476, 38543, 41615, 43631, 44944, 49067, 98762]) * sampling_rate


# for add seizure event + label
main_seizure_only = np.array([])
main_event_only = np.array([])

###########################################
# Interictal: 0, Preictal:1, Ictal: 2     #
# Manual #
# 2 Cases ( 1. Enough gap ( > 3hrs ) 2. Not Enough ( 1. < 1 hr  2. < 3 hrs ( same code ))) #

# Seizure 0 ( Less ) 
seizure_period_0 = main_all_concat[:,seizure_start_info[0]-10800*sampling_rate: seizure_stop_info[0]]
event_period_0   = np.zeros([1, seizure_period_0.shape[1]])
event_period_0[0][-((3600+29) * sampling_rate): -(29 * sampling_rate + 1)] = 1
event_period_0[0][-(29 * sampling_rate):] = 2
print(f'{(seizure_period_0.shape)} = {(event_period_0.shape)}')
print(f'Count 0 in event_period_0: {np.count_nonzero(event_period_0==0)}')
print(f'Count 1 in event_period_0: {np.count_nonzero(event_period_0==1)}')
print(f'Count 2 in event_period_0: {np.count_nonzero(event_period_0==2)}')
print("-----------------------------------------------------------------")

# Seizure 1 ( Less ) 
seizure_period_1 = main_all_concat[:, seizure_stop_info[0]: seizure_stop_info[1]]
event_period_1   = np.zeros([1, seizure_period_1.shape[1]])
event_period_1[0][-((3600+30) * sampling_rate): -(30 * sampling_rate + 1)] = 1
event_period_1[0][-(30 * sampling_rate):] = 2
print(f'Count 0 in event_period_1: {np.count_nonzero(event_period_1==0)}')
print(f'Count 1 in event_period_1: {np.count_nonzero(event_period_1==1)}')
print(f'Count 2 in event_period_1: {np.count_nonzero(event_period_1==2)}')
print("-----------------------------------------------------------------")

# Seizure 2 ( Less ) 
seizure_period_2 = main_all_concat[:, seizure_stop_info[1]: seizure_stop_info[2]]
event_period_2   = np.zeros([1, seizure_period_2.shape[1]])
event_period_2[0][: -(39 * sampling_rate + 1)] = 1
event_period_2[0][-(39 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_2==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_2==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_2==2)}')
print("-----------------------------------------------------------------")

# Seizure 3 ( Less ) 
seizure_period_3 = main_all_concat[:, seizure_stop_info[2] : seizure_stop_info[3]]
event_period_3   = np.zeros([1, seizure_period_3.shape[1]])
event_period_3[0][: -(38 * sampling_rate + 1)] = 1
event_period_3[0][-(38 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_3==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_3==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_3==2)}')
print("-----------------------------------------------------------------")

# Seizure 4 ( Less ) 
seizure_period_4 = main_all_concat[:, seizure_stop_info[3]: seizure_stop_info[4]]
event_period_4   = np.zeros([1, seizure_period_4.shape[1]])
event_period_4[0][: -(35 * sampling_rate + 1)] = 1
event_period_4[0][-(35 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_4==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_4==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_4==2)}')
print("-----------------------------------------------------------------")

# Seizure 5 ( Less ) 
seizure_period_5 = main_all_concat[:, seizure_stop_info[4]: seizure_stop_info[5]]
event_period_5   = np.zeros([1, seizure_period_5.shape[1]])
event_period_5[0][: -(49 * sampling_rate + 1)] = 1
event_period_5[0][-(49 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_5==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_5==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_5==2)}')
print("-----------------------------------------------------------------")

# Seizure 6 ( Less ) 
seizure_period_6 = main_all_concat[:, seizure_stop_info[5]: seizure_stop_info[6]]
event_period_6   = np.zeros([1, seizure_period_6.shape[1]])
event_period_6[0][-((3600+35) * sampling_rate): -(35 * sampling_rate + 1)] = 1
event_period_6[0][-(35 * sampling_rate):] = 2
print(f'Count 0 in event_period_2: {np.count_nonzero(event_period_6==0)}')
print(f'Count 1 in event_period_2: {np.count_nonzero(event_period_6==1)}')
print(f'Count 2 in event_period_2: {np.count_nonzero(event_period_6==2)}')
print("-----------------------------------------------------------------")

# Seizure 7 ( More ) 
seizure_period_7 = main_all_concat[:, seizure_start_info[7] - 10800*sampling_rate: seizure_stop_info[7]]
event_period_7   = np.zeros([1, seizure_period_7.shape[1]])
event_period_7[0][-((3600+39) * sampling_rate): -(39 * sampling_rate + 1)] = 1
event_period_7[0][-(39 * sampling_rate):] = 2
print(f'Count 0 in event_period_7: {np.count_nonzero(event_period_7==0)}')
print(f'Count 1 in event_period_7: {np.count_nonzero(event_period_7==1)}')
print(f'Count 2 in event_period_7: {np.count_nonzero(event_period_7==2)}')
print("-----------------------------------------------------------------")
#-------------------------------------------------------------------------------------------------------------#

# Stack seizure with event
main_seizure_only = np.hstack((seizure_period_0, seizure_period_1, seizure_period_2, seizure_period_3, seizure_period_4, seizure_period_5, seizure_period_6, seizure_period_7))
main_event_only  = np.hstack((event_period_0, event_period_1, event_period_2, event_period_3, event_period_4, event_period_5, event_period_6, event_period_7))
data_with_event = np.vstack((main_seizure_only, main_event_only))
# print(data_with_event[2])

# Debugging line
print(f'Count 2: {np.count_nonzero(data_with_event[-1]==2)}')
print(f'data array stacked shape is: {data_with_event.shape}')
# Delete variable
del main_all_concat, main_seizure_only
print("--------Done Stacking Array--------")


def count_shifted_window(x):
    second = int(x/256)
    array = np.arange(second)  # Count window

    start = 0
    end = 8
    # end = 40
    count = 0

    while (end <= array[-1]):
        sub = array[start:end]
        # print(sub)
        count+=1
        start = start + 4
        end += 4
        del sub
    return count

for i in range(4):
    data_with_event[i] = (data_with_event[i]-np.min(data_with_event[i]))/(np.max(data_with_event[i])-np.min(data_with_event[i]))

# Entropy Initialize
entropy_array = np.zeros((5, int(data_with_event.shape[1]/(sampling_rate*overlapping))))
print(f"Shape entropy is {entropy_array.shape}")
# Entropy calculation
sig_channal = 4
for i in range(sig_channal+1): # +1 including event
    start = 0                 
    end = window_len * sampling_rate          
    count = 0
    print(f"----Calculating channel {i}----")
    if (i != sig_channal):  
        while (end <= data_with_event.shape[1]):
            # print(f"----GOODBYE channel {i}----")
            sub_data = data_with_event[i][start: end]
            entropy_data = entropy(sub_data) # Shannon Scipy Library
            entropy_array[i][count] = entropy_data
            # start, end = end, end + (overlapping * sampling_rate)
            start = start + (overlapping * sampling_rate)
            end = end + (overlapping * sampling_rate)
            count = count + 1
    else :
        while (end <= data_with_event.shape[1]):
            # print(f"----HELLO channel {i}----")
            entropy_array[i][count] = mode(data_with_event[i][:][start: end], axis=None)[0][0] 
            # print(mode(data_with_event[i][:][start: end], axis=None)[0][0])
            start = start + (overlapping * sampling_rate)
            end = end + (overlapping * sampling_rate)
            count = count + 1

print(entropy_array[0][:10])
print(entropy_array[1][:10])
print(entropy_array[2][:10])
print(entropy_array[3][:10])
print(entropy_array[4][:10])
print(f"Index 0 is {np.where((entropy_array[4])==0)[0][0]}")


# print(f"Nan is {np.where(np.isnan(entropy_array[-1]))[0]}")

print(f"Shape entropy is {entropy_array.shape}")
filename = "entropy-" + patient_chb + "-with-event.npy"
np.save(filename, entropy_array)