import mne
import mne.viz
import numpy as np
import json
from scipy.stats import mode
import pandas as pd

total_median_array = []
total_delta_array = []
shape_check = 0 

for i in range(7, 44):
    if i == 20:
        continue

    fileno = str(i).zfill(2)
    path_median = './chb04_csv_hr/chb04_{}/MEDIAN_04_{}.csv'.format(fileno, fileno)
    path_delta = './chb04_csv_hr/chb04_{}/DELTA_04_{}.csv'.format(fileno,fileno)

    file_number = '_' + fileno
    patient_chb = 'chb04'
    data_median = pd.read_csv(path_median, header=None)
    data_delta = pd.read_csv(path_delta, header=None)

    median_hr_array = np.transpose(data_median.to_numpy())
    delta_hr_array = np.transpose(data_delta.to_numpy())

    print(f'Length of {patient_chb}{file_number} is {median_hr_array.shape[1]}')

    shape_check = shape_check + median_hr_array.shape[1]
    total_median_array = np.append(total_median_array, median_hr_array)
    total_delta_array = np.append(total_delta_array, delta_hr_array)

print(f'Length Delta is {total_delta_array.shape[0]}')
print(f'Length Median is {total_median_array.shape[0]}')

print(f'LLast {total_delta_array[-1]}')
print(f'LLast {total_median_array[-1]}')


print(f'Should equal to {shape_check}')

np.save('./total_array/' + 'total_median_array', total_median_array)
np.save('./total_array/' + 'total_delta_array', total_delta_array)

# Task 
# Median append Median --> 1 numpy
# Delta append Delta --> 1 numpy
# should 247272


