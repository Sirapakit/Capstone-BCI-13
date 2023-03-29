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

                    if(one_stream.name() == "my_stream"):
                        inlet_chn_0 = StreamInlet(one_stream)

                # self.receive_flag.set()

            # add code maxSize 
            self.samples_chn_0 = np.array([])

            # while self.receive_flag.is_set():
            while True:
                self.sub_samples_chn_0, timestamps = inlet_chn_0.pull_chunk()
                # self.sub_samples_chn_1, timestamps = inlet_chn_1.pull_chunk()

                # Extract first index of every sublist
                first_list  = [sublist[0] for sublist in self.sub_samples_chn_0]
                second_list = [sublist[1] for sublist in self.sub_samples_chn_0]
                third_list  = [sublist[2] for sublist in self.sub_samples_chn_0]
                fourth_list = [sublist[3] for sublist in self.sub_samples_chn_0]

                self.final_list = []
                self.final_list.append(first_list)
                self.final_list.append(second_list)
                self.final_list.append(third_list)
                self.final_list.append(fourth_list)
                # print(f"Final List is {self.final_list}"

                # List Flatten
                # self.flat_sub_samples_chn_0 = [item for sublist in self.sub_samples_chn_0 for item in sublist] # List flatten
                # self.flat_sub_samples_chn_1 = [item for sublist in self.sub_samples_chn_1 for item in sublist] # List flatten
              
                # print(f"Channel 0 inlet: {self.flat_sub_samples_chn_0}")
                # print(f"Channel 1 inlet: {self.flat_sub_samples_chn_1}")
                # Channel 0 == Channel 1

                sys.stdout.flush()

                self.queue.put(self.final_list)
                time.sleep(1.00) # 1 = 255 rate

    def count_samples_from_lsl(self):
        # Initialize main chunk
        # self.main_chunk_chn0 = np.array([[]]) 
        self.main_chunk_chn0 = np.empty((4, 0))
        while True:
            if not self.queue.empty():
                self.new_sub_chunk_chn0 = self.queue.get() # get new sub-chunk as list
                # print(f"From queue1 data shape is: {len(self.new_sub_chunk_chn0[0])}")
                
                self.main_chunk_chn0 = np.hstack((self.main_chunk_chn0, self.new_sub_chunk_chn0)) # concat main-chunk with sub-chunk
                # print(f"Shape samples_from_lsl_1 is {self.main_chunk_chn0.shape}") # Shape of main chunk
                
                # Code for cropping to 1024 samples for every main chunk
                if (self.main_chunk_chn0.shape[1] >= 1024): 
                    diff = (self.main_chunk_chn0.shape[1]) - 1024
                    print(f"Diff is {diff}")

                    if (diff == 0):
                        # if main chunk is 1024 samples --> put to queue2
                        self.queue2.put(self.main_chunk_chn0)
                        print(f"Successfully put main chunk to queue2")

                    elif (diff >= 1):
                        # main_chunk = main_chunk[0: -diff]
                        # print(f"Exceeded samples is {self.main_chunk_chn0[:, -diff:] } ")
                        self.put_chunk_chn0 = self.main_chunk_chn0[:, :-diff] 
                        # print(f"Main chunk is {self.main_chunk_chn0}")            # Main chunk before cropping
                        # print(f"Main chunk size is {self.main_chunk_chn0.shape}") # Main chunk before cropping size

                        # crop hstack to 1024 samples --> put to queue2
                        self.queue2.put(self.put_chunk_chn0)
                        # print(f"Put chunk is {self.put_chunk_chn0}")            # Main chunk before cropping
                        print(f"Put chunk size is {self.put_chunk_chn0.shape}") # Main chunk before cropping sizw
                        print(f"Successfully put main chunk to queue2")

                        # main_chunk = main_chunk[-diff:]
                        self.main_chunk_chn0 = self.main_chunk_chn0[:, -diff:]
                        # print(f"Left over chunk is {self.main_chunk_chn0}")               # Main chunk after cropping
                        # print(f"Left over chunk shape is {self.main_chunk_chn0.shape}") # Shape of main chunk after cropping

                    else: 
                        raise KeyError ("Error: Chunk cropping failed")

    def send_data(self):
        self.main_channel_0_roll = np.zeros((4,2048))
        # self.roll_flag.set()
        while True:
            if not self.queue.empty():
                self.queue2_samples_chn_0 = self.queue2.get()

                # print(f"Channel 0 data from queue2 is : \n{self.queue2_samples_chn_0}")
                # print(f"Data size from queue2 is:{self.queue2_samples_chn_0.shape}") # Should be 1024 samples from queue2 (last def)
                
                shift = SAMPLING_FREQ*SHIFTED_DURATION
                for i in range(self.main_channel_0_roll.shape[0]):  # loop over 4 rows
                    self.main_channel_0_roll[i, :] = np.roll(self.main_channel_0_roll[i, :], shift) # np.roll each row individually

                self.main_channel_0_roll[:, SAMPLING_FREQ*SHIFTED_DURATION:] = self.queue2_samples_chn_0

                # print(f"Channel 0 After roll :\n {self.main_channel_0_roll}")
                print(f"Size after roll :{self.main_channel_0_roll.shape}")

                sys.stdout.flush()
                self.queue3.put(self.main_channel_0_roll)
                print(f"Successfully put window to queue3")
    
                # self.put_flag.clear()
                # self.roll_flag.clear()
                time.sleep(1)