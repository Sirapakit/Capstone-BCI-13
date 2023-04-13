import numpy as np
second = int(1738)
array = np.arange(second)  # Count window

start = 0
end = 8

count = 0

while (end <= array[-1]):
    sub = array[start:end]
    count+=1
    start = start + 4
    end += 4
    
print(count)
