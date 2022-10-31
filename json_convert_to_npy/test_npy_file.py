import numpy as np 

path = r'../dataset/chb15/npy/data_chb15_54.npy'
data = np.load(path)

start = [263, 843, 1524, 2179, 3428]
end   = [318, 1020, 1595, 2250, 3460]

def to_sample(second):
    return second * 256


print(data[2][to_sample(start[0]-30):to_sample(start[0])])