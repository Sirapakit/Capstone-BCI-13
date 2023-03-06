import numpy as np

data_path = './8bands-chb02.npy'
array = np.load(data_path)

rand_bands = np.random.randint(low=0, high=array.shape[0]-32+1)
cropped_array = array[rand_bands:rand_bands+32,:]

print("Original shape:", array.shape)
print("Cropped shape:", cropped_array.shape)
