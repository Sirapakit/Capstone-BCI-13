import multiprocessing as mp
import logging
import time
import numpy as np
import time
import pylsl
from typing import List
from pylsl import StreamInlet, resolve_stream
import sys

SAMPLING_FREQ = 256
WINDOW_LENGTH = 8   # sec
NUM_BANDS = 8
OVERLAP_PERCENT = 0.5
SHIFTED_DURATION = 4 # sec

logging.basicConfig(level=logging.INFO)
class sendData():

    # Fp2_F8_data = np.zeros((8),dtype='float64') 
    Fp2_F8_data = np.zeros((SAMPLING_FREQ*WINDOW_LENGTH),dtype='float64') 

    def __init__(self,sample_Fp2_F8,queue,queue2):
        self.sample_Fp2_F8 = sample_Fp2_F8
        self.queue = queue
        self.queue2 = queue2
        # Initialize flagging 
        self.put_flag = mp.Event()
        self.put_flag.clear()

        self.roll_flag = mp.Event()
        self.roll_flag.clear()

    def data_from_lsl(self):
        while True:
            # add code maxSize 
            self.sample_Fp2_F8 = np.array([])
            streams = resolve_stream()

            inlet_Fp2_F8 = StreamInlet(streams[0])
            info = pylsl.StreamInfo()
            count = 0
            count2 = 0
            # while count < (2):  
            # while count < (SAMPLING_FREQ * SHIFTED_DURATION):  # This code pull 4096 samples from LSL 
            # while count < (SAMPLING_FREQ * SHIFTED_DURATION/2):  # This code pull 2048 samples from LSL 
            while count < (SAMPLING_FREQ * SHIFTED_DURATION/4):  # This code pull 1024 samples from LSL 
                for info in streams: 
                    self.sample_in_Fp2_F8, timestamps = inlet_Fp2_F8.pull_sample()
                    # logging.info(f"sample_in_Fp2_F8: {self.sample_in_Fp2_F8}")
                    self.sample_Fp2_F8 = np.hstack((self.sample_Fp2_F8,np.round(self.sample_in_Fp2_F8[0],7)))
                    # logging.info(f"sample_Fp2_F8: {self.sample_Fp2_F8}")
                time.sleep(0.0004)
                count += 1

            logging.info(f"data from lsl {self.sample_Fp2_F8}")
            print(f"Data size from lsl is: {self.sample_Fp2_F8.shape}")

            #-----------------------------------------------#
            # Try to log
            filename = "data-set-" + str(count2) + ".txt"
            np.savetxt(filename, self.sample_Fp2_F8)
            count2 = count2 + 1
            # Should Pull 8 seconds from LSL: failed (pull 16 secs)
            #-----------------------------------------------#

            sys.stdout.flush()
            self.queue.put(self.sample_Fp2_F8)
            self.put_flag.set()
            time.sleep(1)


    def send_data(self):
        count = 0
        self.Fp2_F8_roll = np.zeros(2048)
        # self.roll_flag.set()
        while True:
            if not self.queue.empty():
                self.sample_Fp2_F8 = self.queue.get()
                print(f"Sent data {self.sample_Fp2_F8}")
                print(f"Sample Data size is:{self.sample_Fp2_F8.shape}") # Should be 1024 samples

                # while count_for_roll < 4:
                # while count_for_roll < (SAMPLING_FREQ * SHIFTED_DURATION): # This line should get 2048 samples
                # count_for_roll = 0
                # while count_for_roll < ((SAMPLING_FREQ * SHIFTED_DURATION)): # This line should get 1024 samples: get 1024 samples
                # while self.roll_flag.is_set(): # True = Flag
                # print(f"Sample shape Fp2 F8 is {self.sample_Fp2_F8.shape}")
                self.Fp2_F8_roll = np.roll(self.Fp2_F8_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                self.Fp2_F8_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.sample_Fp2_F8
                # self.Fp2_F8_data = self.Fp2_F8_roll
                print(f"After roll :{self.Fp2_F8_roll}")
                print(f"Size: :{self.Fp2_F8_roll.shape}")
                # print(f"Last index After roll {count_for_roll} :{self.Fp2_F8_data[-10:]}")
                # count_for_roll  += 256

                # logging.info(f"data from roll {self.Fp2_F8_data}")
                sys.stdout.flush()
                self.queue2.put(self.Fp2_F8_data)
                # self.put_flag.clear()
                # self.roll_flag.clear()
                # logging.info(f"Sent data {self.Fp2_F8_data}")

                #-----------------------------------------------#
                # should pull data forward --> pull backward
                # Try to log
                filename = "send-data-" + str(count) + ".txt"
                np.savetxt(filename, self.Fp2_F8_data)
                # Will print same samples for 256 times 
                # ex. 1 1 ... 1 ( 256 samples ) 2 2 ... 2 ( 256 samples )
                # the samples is consecutive but redundant for 256 samples
                count = count + 1
                #-----------------------------------------------#

                time.sleep(1)