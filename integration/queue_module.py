from multiprocessing import Queue
import multiprocessing as mp
from sender import sendData
from receiver import receiveData
import numpy as np
import sys

if __name__ =='__main__':
    mp.freeze_support()
    queue = Queue()
    send = sendData(np.array([]),queue)
    # receive = receiveData(queue)

    p1 = mp.Process(target=send.data_from_lsl)
    p2 = mp.Process(target=send.send_data)

    # p3 = mp.Process(target=receive.receive_data)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
