import mne
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# data = np.load('../convert-all-channel-edf/edf-concat/chb03/chn16-chb03.npy')
# data =  np.load('../convert-all-channel-edf/edf-concat/chb01/chn4-chb01.npy')
data =  np.load('../convert-all-channel-edf/edf-concat/chb06/chn17-chb06.npy')
# data =  np.load('../convert-all-channel-edf/edf-concat/chb03/chn12-chb03.npy')


sampling_rate = 256
window_len = 8
overlapping = 4

# chb01
# seizure_start_info = np.array([10196, 12267, 52132, 55015, 62920, 71390, 90925]) * sampling_rate
# seizure_stop_info  = np.array([10236, 12294, 52172, 55066, 63010, 71483, 91026]) * sampling_rate

# chb03
# seizure_start_info = np.array([362, 4331, 7632, 9794, 120788, 124998, 127731]) * sampling_rate
# seizure_stop_info  = np.array([414, 4396, 7701, 9846, 120835, 125062, 127784]) * sampling_rate 

# chb06 
seizure_start_info = np.array([1724, 21888, 42352, 43554, 49438, 126588, 139321, 157794, 225717, 235233]) * sampling_rate
seizure_stop_info  = np.array([1738, 21903, 42367, 43574, 49458, 126604, 139333, 157807, 225729, 235249]) * sampling_rate



def tsallis_entropy(array, q):
  values, counts = np.unique(array, return_counts=True)
  probs = counts / sum(counts)
  return (1 - sum(p**q for p in probs)) / (q - 1)

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
  return count


data = (data-np.min(data))/(np.max(data)-np.min(data))
entropy_array = np.zeros(int(data.shape[0]/(sampling_rate*overlapping)))

start = 0                 
end = window_len*sampling_rate          
count = 0
while (end <= data.shape[0]):
    sub_data = data[start: end]
    entropy_data = entropy(sub_data) # Shannon Library
    # entropy_data = np.sum(sub_data * np.log10(sub_data)) * -1  # Shannon Hard Code
    # entropy_data = tsallis_entropy(sub_data, 2) # Tsallis Entropy 
    # less sensitive to the probability of low-frequency values.
    entropy_array[count] = entropy_data
    start, end = end, end + (overlapping * sampling_rate)
    count = count + 1


############################################################
def moving_average(a, n=10) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
############################################################
# chb01 0, 2, last 6

# chb06 1, 2, 5

# chb03 1


entropy_array = entropy_array[3:10000]
seizure = 1
plt.plot(entropy_array)
# plt.plot(moving_average(entropy_array))
# print(f'Data is {entropy_array[count_shifted_window(seizure_start_info[seizure])-100: count_shifted_window(seizure_stop_info[seizure])]}')
plt.vlines([count_shifted_window(seizure_start_info[seizure]), count_shifted_window(seizure_stop_info[seizure])], max(entropy_array), min(entropy_array), colors='red', linestyles='dotted')
plt.vlines([count_shifted_window(seizure_start_info[seizure])-898], max(entropy_array), min(entropy_array), colors='green', linestyles='dotted')

# plt.xlim([count_shifted_window(seizure_start_info[seizure])-1798, count_shifted_window(seizure_stop_info[seizure])+100])
# plt.xlim([0, count_shifted_window(seizure_stop_info[seizure])+100])


# plt.ylim(np.min(entropy_array[2447-1798: 2460+100])-0.1, np.max(entropy_array[2447-1798: 2460+100])+0.1)
plt.show()

# 1798 = 1 hour windoe



