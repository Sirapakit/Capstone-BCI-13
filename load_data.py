import numpy as np
import json

f = open('npy_file.json')
path = json.load(f)

data_add = 0
label = 0

for i in path['file_name']:
    data = np.load(i)
    data_add = np.append(data_add,data[0])
    label = np.append(label,data[2])

label = np.delete(label, 0)
# Closing file
f.close()
print(data_add.shape)
print(label.shape)

# Find mode
# from scipy.stats import mode
# a = [0,0,1,1,1,2,2,2]
# most_frequent = mode(a)[0][0]
# most_frequent+1
# mode(a)