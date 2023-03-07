import numpy as np

data1 = np.load('./chb03/chn0-chb03.npy')
data2 = np.load('./chb05-2chn.npy')


print(data1.shape)
print(data2.shape)

data2 = np.round(data2, 7)
print(np.where(data2[:,0] == 1.78e-05))
print(data2[:,0][1376:1376+10])

# print(np.where(data2[:,0] == 1.15e-05))
# print(data2[:,0][1440:1450])

