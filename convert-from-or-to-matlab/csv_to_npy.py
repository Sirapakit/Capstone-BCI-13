

##### DONT USE $$$$
#### FROM CSV --> NUMPY FILE WITH 8 + 8 + 2 ( MED, DELTA ) + 1 


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


fileno = '28'
path_delta = './chb04_csv_hr/chb04_{}/DELTA_04_{}.csv'.format(fileno,fileno)
path_median = './chb04_csv_hr/chb04_{}/MEDIAN_04_{}.csv'.format(fileno, fileno)

file_number = '_' + fileno
patient_chb = 'chb04'
data_delta = pd.read_csv(path_delta, header=None)
data_median = pd.read_csv(path_median, header=None)

seizure_info = {'start': 3782, 'stop': 3898}
# Green = Onset start
# Red = Seizure period

xlim = {'start': 3782 -200, 'stop': 3898+ 100}


data_nparray_delta = data_delta.to_numpy()
data_nparray_median = data_median.to_numpy()

data_nparray_delta = (data_nparray_delta-np.min(data_nparray_delta))/(np.max(data_nparray_delta)-np.min(data_nparray_delta))
data_nparray_median = (data_nparray_median-np.min(data_nparray_median))/(np.max(data_nparray_median)-np.min(data_nparray_median))


plt.plot(data_nparray_delta)
plt.title('Delta HR')
plt.xlim([(xlim['start']/2) , (xlim['stop']/2) ])

plt.vlines(seizure_info['start']/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
plt.vlines(seizure_info['start']/2 , 0, 1, color='red' ,linestyle="dashed")
plt.vlines(seizure_info['stop']/2 , 0, 1, color='red' ,linestyle="dashed")

plt.show()


# save_path = './chb04_only_hr_npy/' + patient_chb + file_number
# filename_delta = 'data_chb04' + file_number + '_delta'
# filename_median = 'data_chb04' + file_number + '_median'

# np.save(os.path.join( save_path, filename_delta ), data_to_numpy_delta)
# np.save(os.path.join( save_path, filename_median ), data_to_numpy_median)
print('############# Sucessfully #############')

######## TEST NUMPY FILE ###########
# path_test_data = './chb04_only_hr_npy/chb04_08/data_chb04_08_delta.npy'
# path_test_data = r'../create_new_filterbank/new_energy_bands/chb04/data_chb04_01_energy_v2.npy'
# test_data = np.load(path_test_data)
# print(f'Shape = {test_data.shape}')
