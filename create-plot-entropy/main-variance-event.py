import numpy as np
from scipy.stats import mode


data_load = np.load('./entropy-chb06-with-event.npy')
chb = "chb06"
sampling_rate = 256

# Check data
print(f"The window length is {data_load.shape} ")

data_cropped = data_load[:, 1:-1]
print(f"The window length is {data_cropped.shape} ")
# print(f"Event array is {data_cropped[-1]}")

window_size = 10
overlapping = 1 
num_window = (data_cropped.shape[1] - window_size) // overlapping + 1

var_arr = np.zeros((4, num_window))
mode_arr = np.zeros(num_window)

for i in range(num_window):
    start = i * overlapping
    end = start + window_size
    window = data_cropped[:, start:end]

    last_row = window[-1]
    mode_data = mode(last_row)[0]
    mode_arr[i] = mode_data

    var = np.var(window[:-1], axis=1)
    var_arr[:, i] = var

print(var_arr)
print(mode_arr)
final_data = np.vstack((var_arr, mode_arr))
print(f"Final Data Shape: {final_data.shape}")

event_chn2 = final_data[-1]
# Find the indices of all 1's and 2's in the array
one_indices = np.where(event_chn2 == 1)[0]
two_indices = np.where(event_chn2 == 2)[0]
print("Indices of 1 Final:", one_indices.shape)
print("Indices of 2 Final:", two_indices.shape)

filename = "variance-" + chb + ".npy"
np.save(filename, final_data)