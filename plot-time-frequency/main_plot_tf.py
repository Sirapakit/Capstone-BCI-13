import numpy as np
import matplotlib.pyplot as plot
import scipy.stats as stats
from matplotlib import colors


data_path = r'/Users/sirap/Documents/Capstone-BCI-13/plot-all-channels/data_chb01_03_all_channels2.npy'
data = np.load(data_path)

sampling_rate = 256
seizure_info = { 'start': 2996, 'stop':3036}
xlim = {'start': 2996 -200, 'stop': 3036+ 100}

# F8_T8_data = data[13] # All
# F8_T8_data = data[13][0 : (2996 -10)* sampling_rate] # Before Seizre
F8_T8_data = data[13][0 : 7500] # Before Seizre ( 7000 )
# F8_T8_data = data[13][(2996 - 30) * sampling_rate: 2996 * sampling_rate] # During Seizure Onset
# F8_T8_data = data[13][2996 * sampling_rate: 3036 * sampling_rate]  # During Seizure 


######### Plot time domain #############
plot.plot(F8_T8_data)
plot.title('F8-T8_channel')
# plot.vlines((seizure_info['start'] - 30) * sampling_rate, -0.002, 1, color='green' ,linestyle="dashed")
# plot.vlines(seizure_info['start'] * sampling_rate, -0.002, 1, color='red' ,linestyle="dashed")
# plot.vlines(seizure_info['stop'] * sampling_rate, -0.002, 1, color='red' ,linestyle="dashed")
plot.xlabel('Sample')
plot.ylabel('Norm Amplitude')


######### Plot time freq #############
fig, ax = plot.subplots()
NFFT = 256
# Pxx, freqs, bins, im = plot.specgram(F8_T8_data, NFFT=NFFT, Fs = sampling_rate, 
#                                     cmap='seismic', noverlap=NFFT/2, vmin = -10, vmax = -10)
Pxx, freqs, bins, im = plot.specgram(F8_T8_data, NFFT=NFFT, Fs = sampling_rate, 
                                    cmap='seismic', noverlap=NFFT/2)
fig.colorbar(im, fraction=0.046, pad=0.04).set_label('Intensity [dB]')
plot.ylim([0, 25])
plot.title("Spectrogram")
plot.xlabel('Time (seconds)')
plot.ylabel('Frequency (Hz)')


######### Plot time freq Z Score #############
print(f'Shape data for Spectrogram is {F8_T8_data.shape}')
print(f'Pxx shape is {Pxx.shape}')
F8_T8_data_zscore = np.zeros((Pxx.shape[0], Pxx.shape[1]))
for i in range(Pxx.shape[0]):
    F8_T8_data_zscore[i] = stats.zscore(Pxx[i][:])
print(f'Z-Score Pxx shape is {np.min(F8_T8_data_zscore)}')

fig, ax = plot.subplots()
# plot.imshow(F8_T8_data_zscore, origin='lower', cmap="seismic")
plot.imshow(F8_T8_data_zscore, origin='lower', cmap="seismic", vmin = -10, vmax = 10)
fig.colorbar(im).set_label('Intensity [dB]')


plot.ylim([0, 25])
plot.title("Z Score Spectrogram")
plot.xlabel('Time (seconds)')
plot.ylabel('Frequency (Hz)')



plot.show()   

# x = np.arange(0, 10, .1)
# y = np.arange(0, 10, .1)
# X, Y = np.meshgrid(x,y)

# def do_plot(n, title):
#     #plt.clf()
#     plot.subplot(1, 3, n)
#     plot.pcolor(X, Y, F8_T8_data_zscore, cmap='seismic', vmin=-4, vmax=4)
#     plot.title(title)
#     plot.colorbar()

# plot.figure()
# do_plot(1 ,"all")
# do_plot(2, "<0")
# do_plot(3,  ">0")
# plot.show()