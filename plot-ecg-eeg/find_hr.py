import matplotlib.pyplot as plt
import numpy as np
import heartpy as hp

path_chb04_08 = r'/Users/sirap/Documents/Capstone-BCI-13/dataset/chb04/with-ecg/data_chb04_08.npy'
path_chb04_28 = r'/Users/sirap/Documents/Capstone-BCI-13/dataset/chb04/with-ecg/data_chb04_28.npy'
data_08 = np.load(path_chb04_08)
data_28 = np.load(path_chb04_28)

data_08_info = {
        "start": [6446],
        "end": [6557]
    }
sample_rate = 256
# ecg_signal = data_08[3]
ecg_signal = data_08[3][1000 * 256: 1010 * 256]

plt.figure(1)
plt.tight_layout(h_pad=2)
plt.grid()
# plt.xlim([1000 * 256, 1010 * 256])
plt.ylim([0.3, 0.7])
plt.title('ECG')
plt.plot(ecg_signal)

# filtered = hp.filter_signal(ecg_signal, cutoff = 0.05, sample_rate = sample_rate, filtertype='notch')

#run analysis
wd, m = hp.process(ecg_signal, sample_rate)

#visualise in plot of custom size
plt.figure(figsize=(12,4))
hp.plotter(wd, m)
#display computed measures
for measure in m.keys():
    print('%s: %f' %(measure, m[measure]))

plt.show()
