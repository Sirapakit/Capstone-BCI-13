import numpy as np
from scipy.stats import mode

path = r'/Users/sirap/Documents/Capstone-BCI-13/create_new_filterbank/new_energy_bands/chb01/data_chb01_03_energy_v2.npy' 
data = np.load(path)

data_first_feat = data
print(data_first_feat.shape)
# print(data_first_feat[0 : 512][:])
# need to calculate energy from 512 sample first then sub_energy_array[0][:] = energy_from [0:512]
# cant pass numpy array in function argument


# array_length = 921600
# sampling_rate = 256
# energy_array = np.zeros((17, 1800))
# band = 8
# chn = 2

# for feat in range(band * chn + 1): 
#     start, end = 0, 512
#     count = 0
#     if (feat != band * chn):
#         while (end <= array_length):
#             new_sub_array = np.zeros((1, 512))
#             new_sub_array = data_first_feat[feat][start: end]
#             energy_one_band = np.sum(np.power(new_sub_array, 2))
#             energy_array[feat][count] = energy_one_band
#             start, end = end, end + 512
#             count += 1
#     else : 
#         while (end <= array_length):
#             energy_array[feat][count] = mode(data_first_feat[feat][start: end], axis=None)[0][0] 
#             start, end = end, end + 512
#             count += 1

    
# print(f'Event 0 is {np.count_nonzero(energy_array[-1]==0)}')
# print(f'Event 1 is {np.count_nonzero(energy_array[-1]==1)}')
# print(f'Event 2 is {np.count_nonzero(energy_array[-1]==2)}')


