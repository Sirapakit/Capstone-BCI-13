import numpy as np
load = np.load('data_chb01_01_8bands.npy')
data = load[0:16]
label = load[16]

# convert to vector matrix
start = 0
end = 512
feature = np.zeros((1,8192))
iteration = 10 
for m in range(iteration):
    vec = []
    for k in range(0,16):
        for i in range(start,end):
            vec = np.append(vec,data[k][i])
    vec = np.resize(vec,(1,8192))
    feature = np.append(feature,vec,axis=0)

    # re_label
    re_label = np.zeros((iteration,1))

    label_range = label[start:end]
    a = np.count_nonzero(label_range == 0)
    b = np.count_nonzero(label_range == 1)
    c = np.count_nonzero(label_range == 2)

    if b != 0:
        if b == c:
            re_label[m] = 2
        else:
            re_label[m] = 1

    elif a != b != c:
        d = [a,b,c]
        mode = max(d[:])
        if mode == d[0]:
            re_label[m] = 0

        elif mode == d[1]:
            re_label[m] = 1
            
        else:
            re_label[m] = 2
    
    start = end 
    end += 512
feature = np.delete(feature,0,0)
print(feature.shape)
print(re_label.shape)

# index
# 0 - 511 (12)
# 512 - 1023 (34)
# 1024 - 1535 (56)
# 1536 - 2047 (78)
# 2048 - 2559 (910)
