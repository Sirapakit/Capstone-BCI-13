import numpy as np
import os
import json

data_path = './8bands-chb03.npy'

data_test = np.load(data_path)
print(f'Before selected {data_test.shape[0]}')

f = open('./selected_2chns.json')
info = json.load(f)

rows = np.concatenate([
    np.arange(info["chb01"]["first"][0], info["chb01"]["first"][1]+1),
    np.arange(info["chb01"]["second"][0], info["chb01"]["second"][1]+1),
    [-1]
])

selected_rows = data_test[rows, :]
print(f'After selected {selected_rows.shape[0]}')
f.close()