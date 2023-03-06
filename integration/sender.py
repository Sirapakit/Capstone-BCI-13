import multiprocessing as mp
import logging
import time
import numpy as np
import time
import pylsl
from typing import List
from pylsl import StreamInlet, resolve_stream
import sys

logging.basicConfig(level=logging.INFO)

class sendData():
    Fp2_F8_data = np.zeros((8),dtype='float64') 

    def __init__(self,sample_Fp2_F8,queue):
        self.sample_Fp2_F8 = sample_Fp2_F8
        self.queue = queue


    def data_from_lsl(self):
        while True:
            self.sample_Fp2_F8 = np.array([])
            streams = resolve_stream()

            inlet_Fp2_F8 = StreamInlet(streams[0])
            info = pylsl.StreamInfo()
            count = 0
            while count < (2):  
                for info in streams: 
                    self.sample_in_Fp2_F8, timestamps = inlet_Fp2_F8.pull_sample()
                    # logging.info(f"sample_in_Fp2_F8: {self.sample_in_Fp2_F8}")
                    self.sample_Fp2_F8 = np.hstack((self.sample_Fp2_F8,np.round(self.sample_in_Fp2_F8[0],7)))
                    # logging.info(f"sample_Fp2_F8: {self.sample_Fp2_F8}")
                time.sleep(0.0004)
                count += 1
            logging.info(f"data from lsl {self.sample_Fp2_F8}")
            sys.stdout.flush()
            self.queue.put(self.sample_Fp2_F8)
            time.sleep(1)


    def send_data(self):
        while True:
            
            self.sample_Fp2_F8 = self.queue.get()
            count_for_roll = 0
            while count_for_roll < 4:
                self.Fp2_F8_roll = np.roll(self.Fp2_F8_data, 1)
                self.Fp2_F8_roll[:1] = self.sample_Fp2_F8[count_for_roll]
                self.Fp2_F8_data = self.Fp2_F8_roll
                count_for_roll  += 1
                print(self.Fp2_F8_data)

            # logging.info(f"data from roll {self.Fp2_F8_data}")
            sys.stdout.flush()
            # self.queue.put(self.Fp2_F8_data)
            logging.info(f"Sent data {self.Fp2_F8_data}")
            time.sleep(1)