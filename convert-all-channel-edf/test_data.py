import numpy as np

# data_test = np.load('./test-energy-0-5.npy')
# data_test = np.load('./test-energy-5-9-norm.npy')

# print(f'Original data shape is {data_test.shape}')

# # Cut last Col
# data_test = data_test[:, :-1]

# for i in range(160):
#     data_test[i] = (data_test[i]-np.min(data_test[i]))/(np.max(data_test[i])-np.min(data_test[i]))
# print(f'Shape is {data_test.shape}')
# print(data_test[64])
# print(data_test[75])
# print(np.count_nonzero(data_test[160]==2))

# nan_indices = np.argwhere(np.isnan(data_test))
# print(f'Row that are nan are {np.unique(nan_indices[:, 0])}')

data_test = np.load('./test-energy-13-16.npy')
print(data_test.shape)
