from multiprocessing import Queue
import multiprocessing as mp
from sender import sendData
from receiver import receiveData
import numpy as np
import sys

if __name__ =='__main__':
    mp.freeze_support()
    queue = Queue(maxsize = 2048*15)
    queue2 = Queue(maxsize = 2048*15)
    send = sendData(np.array([]), np.array([]), np.array([]), np.array([]), queue, queue2)
    receive = receiveData(queue2)

    p1 = mp.Process(target = send.data_from_lsl)
    p2 = mp.Process(target = send.send_data)
    p3 = mp.Process(target = receive.process_data)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    

