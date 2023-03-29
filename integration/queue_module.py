from multiprocessing import Queue
import multiprocessing as mp
from sender import sendData
from receiver import receiveData
import numpy as np
import sys

if __name__ =='__main__':
    mp.freeze_support()
    queue  = Queue(maxsize = 2048*10)
    queue2 = Queue(maxsize = 2048*10)
    queue3 = Queue(maxsize = 2048*10)

    send = sendData(np.array([]), np.array([]), np.array([]), np.array([]), queue, queue2, queue3)
    receive = receiveData(queue3)

    p1 = mp.Process(target = send.data_from_lsl)
    p2 = mp.Process(target = send.count_samples_from_lsl)
    p3 = mp.Process(target = send.send_data)
    p4 = mp.Process(target = receive.process_data)

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    

