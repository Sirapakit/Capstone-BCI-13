import numpy as np
import matplotlib.pyplot as plot
import scipy.stats as stats


data_path = r'/Users/sirap/Documents/Capstone-BCI-13/plot-all-channels/data_chb01_03_all_channels2.npy'
data = np.load(data_path)


sampling_rate = 256
# F8_T8_data = data[13] # All
# F8_T8_data = data[13][0 : (2996 -10)* sampling_rate] # Before Seizre
F8_T8_data = data[13][0 : 7500] # Before Seizre ( 7000 )
# F8_T8_data = data[13][(2996 - 30) * sampling_rate: 2996 * sampling_rate] # During Seizure Onset
# F8_T8_data = data[13][2996 * sampling_rate: 3036 * sampling_rate]  # During Seizure 


plot.figure(1)
plot.plot(F8_T8_data)
plot.title('F8-T8_channel')
# plot.vlines(2996 * sampling_rate, -0.002, 1, color='red' ,linestyle="dashed")
# plot.vlines(3036 * sampling_rate, -0.002, 1, color='red' ,linestyle="dashed")
# plot.vlines((2996 - 30) * sampling_rate, -0.002, 1, color='green' ,linestyle="dashed")
plot.xlabel('Sample')
plot.ylabel('Norm Amplitude')


NFFT = 256
fig, ax = plot.subplots()
Pxx, freqs, bins, im = plot.specgram(F8_T8_data, NFFT=NFFT, Fs = sampling_rate, 
                                    cmap='seismic', noverlap=NFFT/2)
fig.colorbar(im).set_label('Intensity [dB]')
plot.ylim([0, 25])
plot.title("Spectrogram")
plot.xlabel('Time (seconds)')
plot.ylabel('Frequency (Hz)')

print(f'Shape data for Spectrogram is {F8_T8_data.shape}')
print(f'Pxx shape is {Pxx.shape}')
# print(f'Freqs: {freqs[0]}')
F8_T8_data_zscore = np.zeros((Pxx.shape[0], Pxx.shape[1]))
for i in range(Pxx.shape[0]):
    F8_T8_data_zscore[i] = stats.zscore(Pxx[i][:])
# print(F8_T8_data_zscore[0])
print(f'Z-Score Pxx shape is {F8_T8_data_zscore.shape}')


fig, ax = plot.subplots()

# plot.rcParams["figure.figsize"] = [17.00, 13.50]
# plot.rcParams["figure.autolayout"] = True
# plot.imshow(F8_T8_data_zscore, origin='lower', cmap="seismic", extent=[0, 1000, -4, 4], aspect=4,)

plot.imshow(F8_T8_data_zscore, origin='lower', cmap="seismic")
fig.colorbar(im).set_label('Intensity [dB]')
plot.ylim([0, 25])
plot.title("Z Score Spectrogram")
plot.xlabel('Time (seconds)')
plot.ylabel('Frequency (Hz)')



plot.show()   
