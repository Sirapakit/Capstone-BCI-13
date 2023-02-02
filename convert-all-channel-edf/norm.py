import numpy as np

data_test0 = np.load('./test-energy-0-5.npy')
data_test1 = np.load('./test-energy-5-9.npy')
data_test2 = np.load('./test-energy-10-14.npy')
data_test3 = np.load('./test-energy-15-19.npy')
data_test4 = np.load('./test-energy-20-22.npy')

print(f'Shape is {data_test1.shape}')
print(f'Shape is {data_test4.shape}')

for i in range(160):
    data_test0[i] = (data_test0[i]-np.min(data_test0[i]))/(np.max(data_test0[i])-np.min(data_test0[i]))
    data_test1[i] = (data_test1[i]-np.min(data_test1[i]))/(np.max(data_test1[i])-np.min(data_test1[i]))
    data_test2[i] = (data_test2[i]-np.min(data_test2[i]))/(np.max(data_test2[i])-np.min(data_test2[i]))
    data_test3[i] = (data_test3[i]-np.min(data_test3[i]))/(np.max(data_test3[i])-np.min(data_test3[i]))

for i in range(96):
    data_test4[i] = (data_test4[i]-np.min(data_test4[i]))/(np.max(data_test4[i])-np.min(data_test4[i]))

np.save('test-energy-0-5-norm.npy',data_test0)
np.save('test-energy-5-9-norm.npy',data_test1)
np.save('test-energy-10-14-norm.npy',data_test2)
np.save('test-energy-15-19-norm.npy',data_test3)
np.save('test-energy-20-22-norm.npy',data_test4)