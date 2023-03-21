import numpy as np
 
# def count_indices(file_path):
#     with open(file_path, 'r') as file:
#         data = file.read()
#         # Split the data string into an array of floats
#         array = [float(x) for x in data.split()]
#         # Return the length of the array
#         return len(array)

# num_indices1 = count_indices("./data-set-0.txt")
# num_indices2 = count_indices("./send2-data2-0.txt")
# print(num_indices1)
# print(num_indices2)


# arr1 = np.arange(1, 4097, 1) # 16 seconds
arr1 = np.arange(1, 15360, 1) # 60 seconds

arr = np.vstack([arr1, arr1, arr1, arr1])
print(arr.shape)

np.save("moke-1-100-data.npy", arr)