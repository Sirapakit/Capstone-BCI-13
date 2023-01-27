import numpy as np
import matplotlib.pyplot as plt

# data = np.load('./test.npy')

# print(data.shape)
 
for i in range(1, 24): 
    exec("main_array_" + str(i) + " = np.array([])")


channel_dict = {}
ch_names = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8-0', 'P8-O2', 'FZ-CZ', 'CZ-PZ', 'P7-T7', 'T7-FT9', 'FT9-FT10', 'FT10-T8', 'T8-P8']
for x in range(23):
    channel_dict["main_array_channel_{0}".format(ch_names[x])] = np.array([])

# print(channel_dict)
a = np.array([1,2,3])
b = np.append(channel_dict["main_array_channel_FP1-F7"], a)
# print(b)


# data_last = np.vstack([value_at_index])


for i in range(3): 
    exec(f"main_array_channel_{i} = np.array([])") 

raw_array = [0,1,3,4]
print(raw_array[2])

for i in range(3): 
    exec(f"main_array_channel_{i} = np.append(main_array_channel_{i}, raw_array{[i]})") 
    
print(main_array_channel_0)
print(main_array_channel_1)
print(main_array_channel_2)

real_main = np.zeros([3, 1])
print(real_main)
for i in range(3): 
    exec(f"real_main{[i]} = main_array_channel_{i}")  

print(real_main)

# data22= np.load("./test234.npy")
# print(data22.shape)

sampling_rate = 256
seizure_start_info = np.array([18427, 44296, 56327, 60061, 77958]) * sampling_rate
seizure_stop_info  = np.array([18542, 44406, 56423, 60181, 78075]) * sampling_rate

print(seizure_stop_info[0])


arr1 = np.array([0, 0, 0, 0, 0])
arr2 = np.array([1, 1, 1, 1, 1])
arr3 = np.array([2, 2, 2, 2, 2])
arr4 = np.array([3, 3, 3, 3, 3])

arr5 = np.vstack((arr1, arr2, arr3, arr4))

print(f'Array test is {arr5}')

# arr6 = np.vstack([arr1, arr2])
# print(arr6)

arr01 = np.array([[1, 2, 3, 4, 5, 6, 7],
               [1, 2, 3, 4, 5, 6, 7]])

arr02 = np.array([[1, 2, 3, 4, 5, 6, 7],
               [1, 2, 3, 4, 5, 6, 7]])

# arr03 = np.hstack((arr01, arr02))
arr03 = np.vstack([arr01, arr02])
print(arr03)

# event_period_4   = np.zeros([1, len(seizure_period_4)])
# print(len(event_period_4))

b = np.array([[1,2,3],
               [4,5,6],
                [7,8,9]]) 
 
#Vertical columns 
c1 = b[:,0:2] 
 
print(c1)
event_period_0   = np.zeros([1, 3])
print(event_period_0.ndim)


# print(test.ndim)

data_test = np.load('./test-energy-norm.npy')
print(data_test.shape)