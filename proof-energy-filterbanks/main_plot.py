import matplotlib.pyplot as plt
import numpy as np

path = r'/Users/sirap/Documents/Capstone-BCI-13/create_new_filterbank/new_energy_bands/chb01/data_chb01_16_energy_v2.npy'
data = np.load(path)
print(f'Shape is {data.shape}')
print(f'Should be 1: {max(data[15])}')
print(f'Should be 0: {min(data[15])}')

sampling_rate = 256

seizure_info = {'start':1015, 'stop': 1066}
# Green = Onset start
# Red = Seizure period

dash_line = { 'first': 665, 'second': 1001, 'third': 1007}

xlim = {'start': 600, 'stop': 1100}

for i in range(1, 17):
    plt.figure(i)

    # if i > 4:                 # Fixing 
    #     k = i % 4             # Fixing 
    #     plt.subplot(4,1,k)    # Fixing 

    energy_band = data[i - 1]
    plt.tight_layout(h_pad=2)
    plt.grid()

    # Config the graphing and dashlined
    plt.xlim([(xlim['start']/2 - 100) , (xlim['stop']/2 + 100) ])

    # Dash line for seizure
    plt.vlines(seizure_info['start']/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
    plt.vlines(seizure_info['start']/2 , 0, 1, color='red' ,linestyle="dashed")
    plt.vlines(seizure_info['stop']/2 , 0, 1, color='red' ,linestyle="dashed")

    # Dash line for checking
    plt.vlines(dash_line['first']/2 , 0, 1, color='m' ,linestyle="dashed")
    plt.vlines(dash_line['second']/2 , 0, 1, color='m' ,linestyle="dashed")
    plt.vlines(dash_line['third']/2 , 0, 1, color='m' ,linestyle="dashed")

    plt.title(f'Band {i}')
    plt.plot(energy_band, color='b')
plt.show()

# plt.subplot(4,1,2)
# x2 = data[1]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 2 chn 1 ')
# plt.plot(x2, color='b')


# plt.subplot(413)
# x3 = data[2]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 3 chn 1 ')
# plt.plot(x3, color='b')


# plt.subplot(414)
# x4 = data[3]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 4 chn 1 ')
# plt.plot(x4, color='b')



# plt.figure(2)
# plt.subplot(411)
# x1 = data[4]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 5 chn 1 ')
# plt.plot(x1, color='b')

# plt.subplot(412)
# x2 = data[5]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 6 chn 1 ')
# plt.plot(x2, color='b')

# plt.subplot(413)
# x3 = data[6]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 7 chn 1 ')
# plt.plot(x3, color='b')

# plt.subplot(414)
# x4 = data[7]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 8 chn 1 ')
# plt.plot(x4, color='b')



# plt.figure(3)
# plt.subplot(411)
# x1 = data[8]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 1 chn 2 ')
# plt.plot(x1, color='b')

# plt.subplot(412)
# x2 = data[9]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 2 chn 2 ')
# plt.plot(x2, color='b')

# plt.subplot(413)
# x3 = data[10]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 3 chn 2 ')
# plt.plot(x3, color='b')

# plt.subplot(414)
# x4 = data[11]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 4 chn 2 ')
# plt.plot(x4, color='b')



# plt.figure(4)
# plt.subplot(411)
# x1 = data[4]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 5 chn 2 ')
# plt.plot(x1, color='b')

# plt.subplot(412)
# x2 = data[5]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 6 chn 2 ')
# plt.plot(x2, color='b')

# plt.subplot(413)
# x3 = data[6]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 7 chn 2 ')
# plt.plot(x3, color='b')

# plt.subplot(414)
# x4 = data[7]
# plt.tight_layout(h_pad=2)
# plt.grid()
# plt.xlim([(2996/2 - 100) , (3036/2 + 100) ])
# plt.vlines(2996/2 - 30/2, 0, 1, color='green' ,linestyle="dashed")
# plt.vlines(2996/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.vlines(3036/2 , 0, 1, color='red' ,linestyle="dashed")
# plt.title('Band 8 chn 2 ')
# plt.plot(x4, color='b')


# plt.show()