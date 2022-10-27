# save numpy array as npy file
import numpy as np
from random import random as rand
import matplotlib.pyplot as plt


# define data
# data = np.asarray([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])
# save to npy file
# np.save('data.npy', data)

# test = np.load('/Users/sirap/Documents/Capstone-BCI-13/dataset/chb15/npy/data.npy')
test = np.load('/Users/sirap/Documents/Capstone-BCI-13/convert_to_npy/data_ten.npy')
print(type(test))

test_t = np.transpose(test)
print(type(test_t[:, 0].tolist()))
print(f'Correct Array is {test_t[:, 0]}')


for i in range(100):
    # print(test[1][i])
    print(test_t[i,0])

# for k in range(1001):
#     mySample = [test_t[k][i+1] for i in range(1)]
#     print(f'Print mySample {mySample}')
# print(f'PUSH mySample {mySample}')


