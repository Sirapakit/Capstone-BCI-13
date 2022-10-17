import numpy as np

trig = np.zeros((1,25))
time_stamp = { "start":1, "stop":2}

trig[0][10] = time_stamp["start"]
trig[0][20] = time_stamp["stop"]

print(trig)