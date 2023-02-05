import numpy as np
array = np.arange(153)  # Count window

start = 0
end = 8
count = 0

while (end <= array[-1]):
    sub = array[start:end]
    # print(sub)
    count+=1
    start = start + 4
    end += 4
    
print(count)

temp = 3
temp2 = 9
for i in range(temp,temp2):
    print(i)