from multiprocessing import Queue
import multiprocessing as mp
from sender import sendData
from receiver import receiveData

if __name__ =='__main__':
    mp.freeze_support()
    queue = Queue()
    send = sendData(queue)
    receive = receiveData(queue)
    p1 = mp.Process(target=send.send_data)
    p2 = mp.Process(target=receive.receive_data)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

