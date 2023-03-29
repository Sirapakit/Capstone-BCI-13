import statistics
import numpy as np
import matplotlib.pyplot as plt


data_load = np.load('./8bands-chb03-nonorm.npy')
sampling_rate = 256

def find_indexes_jump(arr):
    indexes = {}
    for i in range(1, len(arr)):
        if abs(arr[i] - arr[i-1]) > 1:
            indexes[i] = arr[i]
    return indexes

# Check data
print(f"The window length is {data_load.shape} ")
print(f"Event array is {data_load[-1]}")

event_chn = data_load[-1]
# Find the indices of all 1's and 2's in the array
one_indices = np.where(event_chn == 1)[0]
two_indices = np.where(event_chn == 2)[0]

# print("Indices of 1:", one_indices)
print("Indices of 2:", two_indices)

print("Indices of 1 that have jump:", find_indexes_jump(one_indices))
print("Indices of 2 that have jump:", find_indexes_jump(two_indices))

def plot_vline(input, first_index_of_1, first_index_of_2, last_index_of_2):
    plt.plot(input)
    plt.xlim([((first_index_of_1) - 500), (last_index_of_2)])
    plt.vlines((first_index_of_1), max(input), min(input), colors='green', linestyles='dotted')
    plt.vlines([(first_index_of_2), (last_index_of_2)], max(input), min(input), colors='red', linestyles='dotted')

sig_chn = data_load[13*8]
# threshold = 0.4e-05
# for i in range(len(sig_chn)):
#     if sig_chn[i] > threshold:
#         sig_chn[i] = threshold
# print(f"Max Value is {max(sig_chn)}")

plt.figure(1)
plt.suptitle("CHB03 NEW FEATURES")

plt.subplot(311)
# plt.title(f"Seizure index: 426,   2229,   4933,   6704    9409,   5309    12113,   14816    17520,   19899")
plt.plot(sig_chn)
# plt.vlines([426, 2229, 4933, 6704, 9409, 5309, 12113, 14816, 17520, 19899], max(sig_chn), min(sig_chn), colors='red', linestyles='dotted')
# for first vline go see { Indices of 2: }  -------------------------> then minus 9
# for next and others vline go see { Indices of 2 that have jump } --> then minus 9

plt.subplot(312)
plt.title("Seizure 2")
plot_vline(sig_chn, 1097, 1907, 1923+10)
# first arg  : data = data name
# second arg : value of { Indices of 1 that have jump: }    
# third arg  : -> go look in { Indices of 2: } to get the value after second arg 
# fourth arg : mark third arg in { Indices of 2: } and use the value that have jump  

plt.subplot(313)
plt.title("Seizure 4")
plot_vline(sig_chn, 4260, 5160, 5171)


plt.show()
