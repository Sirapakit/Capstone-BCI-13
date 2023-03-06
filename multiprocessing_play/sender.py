import multiprocessing as mp
import logging
import time
import random

logging.basicConfig(level=logging.INFO)

class sendData():
    def __init__(self,queue):
        self.queue = queue

    def send_data(self):
        count = 0
        while True:
            data = random.randint(1,10)
            self.queue.put(data)
            logging.info(f"Sent data: {data}")
            count += 1
            time.sleep(1)

# if __name__ == '__main__':
#     # mp.set_start_method('spawn')
#     # queue = mp.Queue()
#     queue = queueModule.queue
#     logging.info(f"Using queue: {queue}")

#     p = mp.Process(target=send_data, args=(queue,))
#     p.start()

#     p.join()
