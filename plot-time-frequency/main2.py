import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm

data_path = r'/Users/sirap/Documents/Capstone-BCI-13/plot-all-channels/data_chb01_03_all_channels2.npy'
data = np.load(data_path)

sampling_rate = 256
seizure_info = { 'start': 2996, 'stop':3036}
xlim = {'start': 2996 -200, 'stop': 3036+ 100}

# F8_T8_data = data[13] # All
# F8_T8_data = data[13][0 : 7500] # Before Seizre ( 7000 )
# F8_T8_data = data[13][(seizure_info['start'] - 30) * sampling_rate: seizure_info['start'] * sampling_rate] # During Seizure Onset
F8_T8_data = data[13][2996 * sampling_rate: 3036 * sampling_rate]  # During Seizure 




plt.show()