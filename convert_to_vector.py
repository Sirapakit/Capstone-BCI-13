import numpy as np
import os
from scipy.stats import mode

def shift_data(a, L, S ):  # Window len = L, Stride len/stepsize = S
    nrows = ((a.size-L)//S)+1
    n = a.strides[0]
    return np.lib.stride_tricks.as_strided(a, shape=(nrows,L), strides=(S*n,n))

folder = ['chb01','chb02','chb03','chb04','chb05','chb06','chb07','chb08',
          'chb09','chb10','chb11','chb12','chb13','chb14','chb15','chb16',
          'chb17','chb18','chb19','chb20','chb21','chb22','chb23','chb24']

# create vector files
channel = 2
num_band = 8

path_save_x = "path to save file x"
path_save_y = "path to save file y"

for patient in folder:
  path = "path of chbxx"+patient
  all_files = os.listdir(path)
  x = np.zeros((1,48))
  y = np.zeros((1,1))
  count = 0
  for file_name in all_files:
    data = np.load(path + "/" + file_name)
    count += 1
    for i in range(1,channel*num_band+1):
      globals()[f"b{i}"] = shift_data(data[i-1],3,1)  
    arr = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16]

    for sec in range(data.shape[1]-2):
      # create x (dataset)
      tol = np.concatenate((arr[0][sec],arr[1][sec]),axis=0)
      for band in range(2 ,channel*num_band):
        tol = np.concatenate((tol,arr[band][sec]),axis=0)

      tol = tol.reshape(1,channel*num_band*3)
      x = np.concatenate((x,tol),axis=0)

      # create y (label)
      y_pre = shift_data(data[-1], L = 3, S = 1)
      y = np.concatenate((y, mode(y_pre[sec])[0][0]),axis=None)

  # print(f'{patient}: completed')

  x = np.delete(x,0,0)
  y = np.delete(y,0,0)
  print(f'files count:{count}')
  print(f"data size(x) :{x.shape}")
  print(f"label size(y):{y.shape}")

  np.save(f'{path_save_x}/{patient}_vector_x.npy',x)
  np.save(f'{path_save_y}/{patient}_vector_y.npy',y)
  print(f'file {patient} saved')
  print('----------------------------')


# chb04 = (280830,48)
# med_hr = (280830,)
# del_hr = (280830,)