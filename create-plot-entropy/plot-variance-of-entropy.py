import statistics
import numpy as np
import matplotlib.pyplot as plt


data_load = np.load('./variance-chb06.npy')
sampling_rate = 256

def count_window(x):
    second = int(x/256)
    array = np.arange(second)  # Count window
    start = 0
    end = 8
    count = 0
    while (end <= array[-1]):
        sub = array[start:end]
        count+=1
        start = start + 4
        end += 4
    return count
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

print("Indices of 1:", one_indices)
print("Indices of 2:", two_indices)

print("Indices of 1 that have jump:", find_indexes_jump(one_indices))
print("Indices of 2 that have jump:", find_indexes_jump(two_indices))

def plot_vline(input, first_index_of_1, first_index_of_2, last_index_of_2):
    plt.plot(input)
    plt.xlim([((first_index_of_1) - 300), (last_index_of_2)])
    plt.vlines((first_index_of_1), max(input), min(input), colors='green', linestyles='dotted')
    plt.vlines([(first_index_of_2), (last_index_of_2)], max(input), min(input), colors='red', linestyles='dotted')

sig_chn = data_load[0]
threshold = 0.4e-05
for i in range(len(sig_chn)):
    if sig_chn[i] > threshold:
        sig_chn[i] = threshold
print(f"Max Value is {max(sig_chn)}")

plt.figure(1)
plt.suptitle("CHB06 Shannon Entropy")

plt.subplot(311)
plt.title(f"Seizure index: 426,   2229,   4933,   6704    9409,   5309    12113,   14816    17520,   19899")
plt.plot(sig_chn)
plt.vlines([426, 2229, 4933, 6704, 9409, 5309, 12113, 14816, 17520, 19899], max(sig_chn), min(sig_chn), colors='red', linestyles='dotted')
# for first vline go see { Indices of 2: }  -------------------------> then minus 9
# for next and others vline go see { Indices of 2 that have jump } --> then minus 9

plt.subplot(312)
plt.title("Seizure 4")
plot_vline(sig_chn, 9409, 10310, 10310+10)
# first arg  : data = variance
# second arg : value of { Indices of 1 that have jump: }  ---------------------------> then minus 9        
# third arg  : -> go look in { Indices of 2: } to get the value after second arg ----> then minus 9  
# fourth arg : mark third arg in { Indices of 2: } and use the value that have jump -> then minus 9  

plt.subplot(313)
plt.title("Seizure 5")
plot_vline(sig_chn, 12113, 12113+600, 12113+810)


plt.show()
