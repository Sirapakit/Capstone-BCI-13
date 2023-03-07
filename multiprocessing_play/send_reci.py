import time
import random
import multiprocessing as mp

def send_data(queue):
    while True:
        data = random.randint(1, 100)
        queue.put(data)
        print(f"Sent data: {data}")
        time.sleep(1)

def receive_data(queue):
    count = 0
    while count < 10:
        data = queue.get()
        count += 1
        print(f"Received data: {data}")
    print("Received 10 samples")

if __name__ == '__main__':
    mp.set_start_method('spawn')
    queue = mp.Queue()

    p1 = mp.Process(target=send_data, args=(queue,))
    p1.start()

    p2 = mp.Process(target=receive_data, args=(queue,))
    p2.start()

    p1.join()
    p2.join()
