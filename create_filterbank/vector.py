import numpy as np
load = np.load('../dataset/chb01/filterbank-npy/data_chb01_01_8bands.npy')
data = load[0:16]
label = load[16]

# convert to vector matrix
start = 0
end = 512

sampling = 512
total_band = 8
total_chn = 2
feature = np.zeros((1, sampling * total_band * total_chn))

iteration = 10 # array_length / ( sampling_rate * 2)
for m in range(iteration):
    vec = []
    for k in range(total_band * total_chn): # 0
        for i in range(start,end):  # 0 - 511
            vec = np.append(vec,data[k][i])

    vec = np.resize(vec, (1, sampling * total_band * total_chn))
    feature = np.append(feature, vec, axis=0)

    # re_label
    re_label = np.zeros((iteration,1))

    label_range = label[start:end]
    a = np.count_nonzero(label_range == 0)
    b = np.count_nonzero(label_range == 1)
    c = np.count_nonzero(label_range == 2)

    if a != b != c:
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

    
feature = np.delete(feature, 0, 0)

np.save('test', feature)

print(feature.shape)
print(re_label.shape)

# index
# 0 - 511 (12)
# 512 - 1023 (34)
# 1024 - 1535 (56)
# 1536 - 2047 (78)
# 2048 - 2559 (910)

# 3600 sec --> 1800 set of 2 sec --> 16 features from 0 - 511