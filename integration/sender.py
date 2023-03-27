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

    count_file = 0
    # Fp2_F8_data = np.zeros((8),dtype='float64') 
    Fp2_F8_data = np.zeros((SAMPLING_FREQ*WINDOW_LENGTH),dtype='float64') 

    def __init__(self, samples_chn_0, samples_chn_1, samples_chn_2, samples_chn_3, queue, queue2, queue3):
        # Initialzie for receive samples from LSL 
        self.samples_chn_0 = samples_chn_0
        self.samples_chn_1 = samples_chn_1
        self.samples_chn_2 = samples_chn_2
        self.samples_chn_3 = samples_chn_3

        # Initialize different queue 
        self.queue = queue    # for receive samples from LSL chunk only
        self.queue2 = queue2  # for crop last queue to 1024 samples
        self.queue3 = queue3  # for get last queue2 to roll and send to receiver.py

        # Initialize flagging 
        # Didn't include in the def yet
        self.put_flag = mp.Event()
        self.put_flag.clear()

        self.roll_flag = mp.Event()
        self.roll_flag.clear()

        self.receive_flag = mp.Event()
        self.receive_flag.clear()

    def data_from_lsl(self):
        while True:
            info = pylsl.StreamInfo()
            logging.info(info)

            all_streams_name = resolve_stream()
            if all_streams_name:
                print(f'Found LSL Stream')

                for one_stream in all_streams_name:
                    print(f'Found stream: {one_stream.name()}')

                    if(one_stream.name() == "bipolar_ch0_database"):
                        inlet_chn_0 = StreamInlet(one_stream)
   
                    if(one_stream.name() == "bipolar_ch1_database"):
                        inlet_chn_1 = StreamInlet(one_stream)

                    # if(one_stream.name() == "bipolar_ch2_database"):
                    #     inlet_chn_2 = StreamInlet(one_stream)
                   
                    # if(one_stream.name() == "bipolar_ch3_database"):
                    #     inlet_chn_3 = StreamInlet(one_stream)

                # self.receive_flag.set()

            # add code maxSize 
            self.samples_chn_0 = np.array([])
            self.samples_chn_1 = np.array([])
            # self.samples_chn_2 = np.array([])
            # self.samples_chn_3 = np.array([])

            # while self.receive_flag.is_set():
            while True:
                self.sub_samples_chn_0, timestamps = inlet_chn_0.pull_chunk()
                self.sub_samples_chn_1, timestamps = inlet_chn_1.pull_chunk()

                self.flat_sub_samples_chn_0 = [item for sublist in self.sub_samples_chn_0 for item in sublist] # List flatten
                self.flat_sub_samples_chn_1 = [item for sublist in self.sub_samples_chn_1 for item in sublist] # List flatten


                # if timestamps:
                #     self.samples_chn_0 = np.hstack((self.samples_chn_0, np.round(self.sub_samples_chn_0[0],7)))
                    # self.samples_chn_1 = np.hstack((self.samples_chn_1, np.round(self.sub_samples_chn_1[0],7)))
                    # self.samples_chn_2 = np.hstack((self.samples_chn_2, np.round(self.sub_samples_chn_2[0],7)))
                    # self.samples_chn_3 = np.hstack((self.samples_chn_3, np.round(self.sub_samples_chn_3[0],7)))

                # time.sleep(0.0004)
              
                # print(f"Channel 0 inlet: {self.flat_sub_samples_chn_0}")
                # print(f"Channel 1 inlet: {self.flat_sub_samples_chn_1}")
                # Channel 0 == Channel 1

                sys.stdout.flush()

                # Put those 4 in queue
                self.queue.put(self.flat_sub_samples_chn_0)
                self.queue.put(self.flat_sub_samples_chn_1)
                # self.queue.put(self.samples_chn_2)
                # self.queue.put(self.samples_chn_3)

                time.sleep(1)

    def count_samples_from_lsl(self):
        # self.samples_from_lsl_1 = np.array([]) # main chunk
        # self.samples_from_lsl_0 = np.array([]) # main chunk
        while True:
            self.samples_from_lsl_0 = self.queue.get() # sub chunk 

            print(f"From queue1: {self.samples_from_lsl_0}")

        # while True:
        #     if not self.queue.empty():
        #         self.sub_samples_from_lsl_0 = self.queue.get() # sub chunk 
        #         self.samples_from_lsl_0 =  np.hstack((self.samples_from_lsl_0, self.sub_samples_from_lsl_0)) # concat main-chunk with sub-chunk
        #         print(f"Shape samples_from_lsl_1 is {self.samples_from_lsl_0.shape}") # Shape of main
                
        #         # if (len(main_chunk) >= 1024:):
        #         if (self.samples_from_lsl_0.shape[0] >= 1024): 
        #             diff = (self.samples_from_lsl_0.shape[0]) - 1024

        #             if (diff == 0):
        #                 # if hastack for 1024 samples --> put to queue2
        #                 self.queue2.put(self.samples_from_lsl_0)

        #             elif (diff >= 1):
        #                 # main_chunk = main_chunk[0: -diff]
        #                 self.samples_from_lsl_0 = self.samples_from_lsl_0[0: -diff] 

        #                 # crop hastack to 1024 samples --> put to queue2
        #                 self.queue2.put(self.samples_from_lsl_0)

        #                 # main_chunk = main_chunk[-diff:]
        #                 self.samples_from_lsl_0 = self.samples_from_lsl_0[-diff: ]
        #                 print(f"Shape from LSL after sorting is {self.samples_from_lsl_0.shape}") # Shape of main

        #             else: 
        #                 raise Exception ("Error: Chunk cropping failed")
                

    def send_data(self):
        self.main_channel_0_roll = np.zeros(2048)
        # self.main_channel_1_roll = np.zeros(2048)
        # self.main_channel_2_roll = np.zeros(2048)
        # self.main_channel_3_roll = np.zeros(2048)

        # self.roll_flag.set()
        while True:
            if not self.queue.empty():
                self.queue2_samples_chn_0 = self.queue2.get()
                # self.queue2_samples_chn_1 = self.queue.get()
                # self.queue2_samples_chn_2 = self.queue.get()
                # self.queue2_samples_chn_3 = self.queue.get()

                # print(f"Channel 0 data is : {self.samples_chn_0}")
                # print(f"Channel 1 data is : {self.samples_chn_1}")
                # print(f"Channel 2 data is : {self.samples_chn_2}")
                # print(f"Channel 3 data is : {self.samples_chn_3}")

                print(f"Data size is:{self.queue2_samples_chn_0.shape}") # Should be 1024 samples from queue2 (last def)
                # print(f"Data size is:{self.queue2_samples_chn_1.shape}") # Should be 1024 samples from queue2 (last def)
                # print(f"Data size is:{self.queue2_samples_chn_2.shape}") # Should be 1024 samples from queue2 (last def)
                # print(f"Data size is:{self.queue2_samples_chn_3.shape}") # Should be 1024 samples from queue2 (last def)

                # while count_for_roll < 4:
                # while count_for_roll < (SAMPLING_FREQ * SHIFTED_DURATION): # This line should get 2048 samples
                # count_for_roll = 0
                # while count_for_roll < ((SAMPLING_FREQ * SHIFTED_DURATION)): # This line should get 1024 samples: get 1024 samples
                # while self.roll_flag.is_set(): # True = Flag
                # print(f"Sample shape Fp2 F8 is {self.samples_chn_0.shape}")

                self.main_channel_0_roll = np.roll(self.main_channel_0_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                self.main_channel_0_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.queue2_samples_chn_0

                # self.main_channel_1_roll = np.roll(self.main_channel_1_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                # self.main_channel_1_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.queue2_samples_chn_1

                # self.main_channel_2_roll = np.roll(self.main_channel_2_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                # self.main_channel_2_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.queue2_samples_chn_2

                # self.main_channel_3_roll = np.roll(self.main_channel_3_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                # self.main_channel_3_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.queue2_samples_chn_0

                print(f"Channel 0 After roll :{self.main_channel_0_roll}")
                print(f"Size: :{self.main_channel_0_roll.shape}")
                # print(f"Channel 1 After roll :{self.channel_1_roll}")
                # print(f"Size: :{self.channel_1_roll.shape}")
                # print(f"Channel 2 After roll :{self.channel_2_roll}")
                # print(f"Size: :{self.channel_2_roll.shape}")
                # print(f"Channel 3 After roll :{self.channel_3_roll}")
                # print(f"Size: :{self.channel_3_roll.shape}")

                sys.stdout.flush()
                self.queue3.put(self.main_channel_0_roll)
                # self.queue3.put(self.channel_1_roll)
                # self.queue3.put(self.channel_2_roll)
                # self.queue3.put(self.channel_3_roll)
    
                # self.put_flag.clear()
                # self.roll_flag.clear()
                time.sleep(1)