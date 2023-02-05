import matplotlib.pyplot as plt
import numpy as np

path = r'/Users/sirap/Documents/Capstone-BCI-13/create-plot-entropy/entropy/chb04/data_chb04_28_energy_v2.npy'
data = np.load(path)
print(f'Shape is {data.shape}')

print(data[1])
print(f'Should be 1: {max(data[15])}')
print(f'Should be 0: {min(data[15])}')

sampling_rate = 256

seizure_info = {'start': 1679, 'stop': 1781}
# Green = Onset start
# Red = Seizure period

# dash_line = { 'first': 665, 'second': 1001, 'third': 1007}

xlim = {'start': 1679 -200, 'stop': 1781+ 100}

for i in range(1, 17):

    if i >= 1 and i <= 4:
        j = 1
        k = i
        plt.figure(j)
    
    if i >= 5 and i <= 8:
        j = 2
        k = i - 4*1
        plt.figure(j)

    if i >= 9 and i <= 12:
        j = 3
        k = i - 4*2
        plt.figure(j)

    if i >= 13 and i <= 16:
        j = 4
        k = i - 4*3
        plt.figure(j)

    plt.subplot(4,1,k)    

    energy_band = data[i - 1]
    plt.tight_layout(h_pad=2)
    plt.grid()

    # Config the graphing and dashlined
    plt.xlim([(xlim['start']/2) , (xlim['stop']/2) ])

    # Dash line for seizure
    plt.vlines(seizure_info['start']/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
    plt.vlines(seizure_info['start']/2 , 0, 1, color='red' ,linestyle="dashed")
    plt.vlines(seizure_info['stop']/2 , 0, 1, color='red' ,linestyle="dashed")

    # # Dash line for checking
    # plt.vlines(dash_line['first']/2 , 0, 1, color='m' ,linestyle="dashed")
    # plt.vlines(dash_line['second']/2 , 0, 1, color='m' ,linestyle="dashed")
    # plt.vlines(dash_line['third']/2 , 0, 1, color='m' ,linestyle="dashed")

    plt.title(f'Band {i}')
    plt.plot(energy_band, color='b')

plt.show()

print(f'Difference: {data[0][1000 : 1010] - data[1][1000 : 1010]}')