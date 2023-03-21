import mne
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

# data_file = r'/Users/sirap/Documents/Capstone-BCI-13/create-plot-entropy/entropy/chb04/data_chb04_28_energy_v2.npy'
data_file = r'/Users/sirap/Documents/Capstone-BCI-13/dataset/chb01/chb01_03.edf'

raw = mne.io.read_raw(data_file)
raw_array = raw.get_data()
array_length = raw_array.shape[1]

seizure_info = { 'start': 2996, 'stop':3036}
xlim = {'start': 2996 -200, 'stop': 3036+ 100}

start = 0 * 256                  #3782#1679
end = 2 * 256                    #3798#1781
count = 0

mock_data = raw_array[13]
mock_data = (mock_data-np.min(mock_data))/(np.max(mock_data)-np.min(mock_data))

entropy_array = np.zeros(int(array_length/512))

def find_entropy(array):
  values, counts = np.unique(array, return_counts=True)
  probs = counts / sum(counts)
  return -sum(p * np.log2(p) for p in probs)

def tsallis_entropy(array, q):
  values, counts = np.unique(array, return_counts=True)
  probs = counts / sum(counts)
  return (1 - sum(p**q for p in probs)) / (q - 1)

def log_energy_entropy(array):
  energy = sum(abs(x)**2 for x in array)
  return np.log2(energy)

while (end <= array_length):
    sub_data = mock_data[start: end]
    # entropy_data = entropy(sub_data) # Shannon Library
    # entropy_data = np.sum(sub_data * np.log10(sub_data)) * -1  # Shannon Hard Code
    # entropy_data = find_entropy(sub_data) # Entropy def 
    # Renyi_entropy = Generalized version of Shannon
    entropy_data = tsallis_entropy(sub_data, 2) # Tsallis Entropy 
    # less sensitive to the probability of low-frequency values.
    # entropy_data = log_energy_entropy(sub_data) # log energy 
    entropy_array[count] = entropy_data
    start, end = end, end + 2 * 256
    count = count + 1

print(entropy_array.shape)

 # Dash line for seizure
plt.vlines(seizure_info['start']/2 - 30/2, min(entropy_array), max(entropy_array), color='green' ,linestyle="dashed")
plt.vlines(seizure_info['start']/2 , min(entropy_array), max(entropy_array), color='red' ,linestyle="dashed")
plt.vlines(seizure_info['stop']/2 , min(entropy_array), max(entropy_array), color='red' ,linestyle="dashed")


print(f'max: {max(entropy_array)}, min: {min(entropy_array)}')
plt.xlim([(xlim['start']/2) , (xlim['stop']/2) ])

plt.grid()
plt.plot(entropy_array)
plt.show()

