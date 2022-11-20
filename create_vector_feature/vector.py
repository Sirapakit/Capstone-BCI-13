import numpy as np
load = np.load('data_chb01_01_8bands.npy')
data = load[0:16]
label = load[16]

# convert to vector matrix
start = 0
end = 512
feature = np.zeros((1,8192))
for m in range(5):
    vec = []
    for k in range(0,16):
        for i in range(start,end):
            vec = np.append(vec,data[k][i])
    vec = np.resize(vec,(1,8192))
    feature = np.append(feature,vec,axis=0)
    start = end 
    end += 512
feature = np.delete(feature,0,0)
print(feature)
print(data[0][2048],data[-1][2559])

# index
# 0 - 511 (12)
# 512 - 1023 (34)
# 1024 - 1535 (56)
# 1536 - 2047 (78)
# 2048 - 2559 (910)

