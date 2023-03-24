import numpy as np
import matplotlib.pyplot as plt

data_load = np.load('./entropy-chb20-with-event.npy')
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

sig_chn_cropped_event = data_load[-1][1:-1]
# Find the indices of all 1's and 2's in the array
one_indices = np.where(sig_chn_cropped_event == 1)[0]
two_indices = np.where(sig_chn_cropped_event == 2)[0]

# print("Indices of 1:", one_indices)
print("Indices of 2:", two_indices)

print("Indices of 1 that have jump:", find_indexes_jump(one_indices))
print("Indices of 2 that have jump:", find_indexes_jump(two_indices))

# np.savetxt("index-of-1.txt", one_indices)
# np.savetxt("index-of-2.txt", two_indices)

def plot_vline(input, first_index_of_1, first_index_of_2, last_index_of_2):
    plt.plot(input)
    plt.xlim([(first_index_of_1 - 500), (last_index_of_2)])
    plt.vlines(first_index_of_1, max(input), min(input), colors='green', linestyles='dotted')
    plt.vlines([first_index_of_2, last_index_of_2], max(input), min(input), colors='red', linestyles='dotted')

### Need to calculate new VLINE Because the data is cropped
### Must use 0, 1, 2 Label to plot
sig_chn_cropped = data_load[0][1:-1]
plt.figure(1)
plt.suptitle("CHB20 Shannon Entropy")

plt.subplot(311)
plt.title("Seizure 1")
plot_vline(sig_chn_cropped, 3035, 3935, 3941)

plt.subplot(312)
plt.title("Seizure 3")
plot_vline(sig_chn_cropped, 4209, 4968, 4976)

plt.subplot(313)
plt.title("Seizure 7")
plot_vline(sig_chn_cropped, 8640, 9540, 9548)


plt.show()
