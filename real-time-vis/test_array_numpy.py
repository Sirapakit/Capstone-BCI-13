import numpy as np

arr = np.array( [[ 1, 2, 3], [2, 4, 6]] )
 
# Printing type of arr object
print("Array is of type: ", type(arr))

all_X = []
all_y = []

for i in arr:
    for j in i:
        all_X.append(j)
print(f'Now X is {all_X}')

