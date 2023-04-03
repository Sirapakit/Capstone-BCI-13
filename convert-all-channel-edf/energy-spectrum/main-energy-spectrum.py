import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt

patient_chb = "chb02"
data = np.load(f'../8bands-nonorm/{patient_chb}/8bands-{patient_chb}-data-crop.npy')
print(f"Data shape is {data.shape}")
raw_signal = data[12]

windowed_signal = raw_signal * np.hamming(len(raw_signal))

fft_signal = fft(windowed_signal)

power_spectrum = np.abs(fft_signal)**2
freqs = np.fft.fftfreq(len(windowed_signal))
freqs = np.abs(freqs[:len(freqs)//2]) * (256)

# print(power_spectrum[:len(power_spectrum)//2].shape)
# print((power_spectrum[:len(power_spectrum)//2].shape[0])/128)
# print(freqs.shape)

plt.plot(freqs, power_spectrum[:len(power_spectrum)//2])
plt.xlabel('Frequency (Hz)')
plt.xlim([0, 30])
plt.ylabel('Power')
plt.show()

# Initialize # CHB03: C4-P4
z0    = 0*(power_spectrum[:len(power_spectrum)//2].shape[0])/128    # 0.0 
z2_5  = 2.5*(power_spectrum[:len(power_spectrum)//2].shape[0])/128  # 69105.0 
z5    = 5*(power_spectrum[:len(power_spectrum)//2].shape[0])/128    # 138210.0
z7_5  = 7.5*(power_spectrum[:len(power_spectrum)//2].shape[0])/128  # 207315.0
z10   = 10*(power_spectrum[:len(power_spectrum)//2].shape[0])/128   # 276420.0
z12_5 = 12.5*(power_spectrum[:len(power_spectrum)//2].shape[0])/128 # 345525.0
z15   = 15*(power_spectrum[:len(power_spectrum)//2].shape[0])/128   # 414630.0
z17_5 = 17.5*(power_spectrum[:len(power_spectrum)//2].shape[0])/128 # 483735.0
z20   = 20*(power_spectrum[:len(power_spectrum)//2].shape[0])/128   # 552840.0
z22_5 = 22.5*(power_spectrum[:len(power_spectrum)//2].shape[0])/128 # 621945.0
z25   = 25*(power_spectrum[:len(power_spectrum)//2].shape[0])/128   # 691050.0
z27_5 = 27.5*(power_spectrum[:len(power_spectrum)//2].shape[0])/128 # 760155.0
z30   = 30*(power_spectrum[:len(power_spectrum)//2].shape[0])/128   # 829260.0

power = power_spectrum[:len(power_spectrum)//2]

# 0-5 Hz
power0_5 = power[int(z0): int(z5)]
mean0_5 = np.mean(power0_5)
print(f"First Band {mean0_5}")

# 2.5-7.5 Hz
power2_5_7_5 = power[int(z2_5): int(z7_5)]
mean2_5_7_5 = np.mean(power2_5_7_5)
print(f"Second Band {mean2_5_7_5}")

# 5-10 Hz
power5_10 = power[int(z5): int(z10)]
mean5_10 = np.mean(power5_10)
print(f"Third Band {mean5_10}")

# 7.5-12.5 Hz
power7_5_12_5 = power[int(z7_5): int(z12_5)]
mean7_5_12_5 = np.mean(power7_5_12_5)
print(f"Fourth Band {mean7_5_12_5}")

# 10-17.5 Hz
power10_17_5 = power[int(z10): int(z17_5)]
mean10_17_5 = np.mean(power10_17_5)
print(f"Fifth Band {mean10_17_5}")

# 15-20 Hz
power15_20= power[int(z15): int(z20)]
mean15_20 = np.mean(power15_20)
print(f"Sixth Band {mean15_20}")

# 17.5-22.5 Hz
power17_5_22_5 = power[int(z17_5): int(z22_5)]
mean17_5_22_5 = np.mean(power17_5_22_5)
print(f"Seventh Band {mean17_5_22_5}")

# 20 - 25 Hz
power20_25 = power[int(z20): int(z25)]
mean20_25 = np.mean(power20_25)
print(f"Eight Band {mean20_25}")

# Relative Power 
print(f"---------Patient {patient_chb}-----------")
print(f"Relative 1/2: {mean0_5/mean2_5_7_5}")
print(f"Relative 1/3: {mean0_5/mean5_10}")
print(f"Relative 1/4: {mean0_5/mean7_5_12_5}")
print(f"Relative 1/5: {mean0_5/mean10_17_5}")
print(f"Relative 1/6: {mean0_5/mean15_20}")
print(f"Relative 1/7: {mean0_5/mean17_5_22_5}")
print(f"Relative 1/8: {mean0_5/mean20_25}")


