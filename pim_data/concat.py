import numpy as np


data1 = np.load('./chb03/chn1-chb03.npy')
data2 = np.load('./chb03/chn5-chb03.npy')
data3 = np.load('./chb03/chn7-chb03.npy')
data4 = np.load('./chb03/chn13-chb03.npy')

data_final = np.vstack((data1, data2, data3, data4))

print(f"Before concat: {data1.shape}")
print(f"After concat: {data_final.shape}")

np.save("chb03-4chn-significant-stream.npy", data_final)