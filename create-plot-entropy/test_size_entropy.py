import matplotlib.pyplot as plt
import numpy as np

data_path = '../convert-all-channel-edf/8bands-chb10-new.npy'
data = np.load(data_path)

print(data.shape)

event = data[-1]
print(f"Event is :{event}")

zero_indices = np.where(event == 0)[0]
print(f"Event id 0 is :{zero_indices.shape}")

one_indices = np.where(event == 1)[0]
print(f"Event id 1 is :{one_indices.shape}")

two_indices = np.where(event == 2)[0]
print(f"Event id 2 is :{two_indices.shape}")

print("------------ Comparing to ------------")

data_path2 = './entropy-chb10-with-event.npy'
data2 = np.load(data_path2)

print(data2.shape)

event2 = data2[-1]

print(f"Event is :{event2}")

zero_indices2 = np.where(event2 == 0)[0]
print(f"Event id 0 is :{zero_indices2.shape}")

one_indices2 = np.where(event2 == 1)[0]
print(f"Event id 1 is :{one_indices2.shape}")

two_indices2 = np.where(event2 == 2)[0]
print(f"Event id 2 is :{two_indices2.shape}")

