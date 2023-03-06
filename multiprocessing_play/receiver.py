import multiprocessing as mp
import logging

logging.basicConfig(level=logging.INFO)

class receiveData():
    def __init__(self,queue):
        self.queue = queue
        
    def receive_data(self):
        count = 0
        while count < 10:
            if not self.queue.empty():
                data = self.queue.get()
                logging.info(f"Received data: {data}")
                count += 1

        logging.info("Received 10 samples. Stopping receive_data.")

# if __name__ == '__main__':
#     # mp.set_start_method('spawn')
#     # queue = mp.Queue()
#     queue = queueModule.queue
#     logging.info(f"Using queue: {queue}")

#     p = mp.Process(target=receive_data, args=(queue,))
#     p.start()

#     p.join()


"""
class Main
    queue = Queue()
    receive = receive(queue)
    send = send(queue)


class receive(queue)



"""