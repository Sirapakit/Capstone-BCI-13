import numpy as np

test = np.load('/Users/sirap/Documents/Capstone-BCI-13/dataset/chb15/npy/data_15.npy')
# print(type(test))
# print(test[0][:])

a = np.array([ 0, 1,  2,  3,  4,  5,  6,  7,  8,  9, 10])
print(a)

def strided_app(a, L, S ):  # Window len = L, Stride len/stepsize = S
    nrows = ((a.size-L)//S)+1
    n = a.strides[0]
    return np.lib.stride_tricks.as_strided(a, shape=(nrows,L), strides=(S*n,n))

b = strided_app(a, L = 5, S = 3)
print(b.shape)
print(b)

# count = (len(a) + ((5 - 3)*2))/5
count = (len(a) + ((5 - 3)*(count-1)))/5

print(count)