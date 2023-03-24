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

    def __init__(self, samples_chn_0, samples_chn_1, samples_chn_2, samples_chn_3, queue, queue2):
        self.samples_chn_0 = samples_chn_0
        self.samples_chn_1 = samples_chn_1
        self.samples_chn_2 = samples_chn_2
        self.samples_chn_3 = samples_chn_3

        # Initialize different queue 
        self.queue = queue    # for receive LSL
        self.queue2 = queue2  # for roll and send to receiver

        # Initialize flagging 
        # Didn't include in the def yet
        self.put_flag = mp.Event()
        self.put_flag.clear()

        self.roll_flag = mp.Event()
        self.roll_flag.clear()

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
                        
                    # if(one_stream.name() == "bipolar_ch1_database"):
                    #     inlet_chn_1 = StreamInlet(one_stream)

                    # if(one_stream.name() == "bipolar_ch2_database"):
                    #     inlet_chn_2 = StreamInlet(one_stream)
                   
                    # if(one_stream.name() == "bipolar_ch3_database"):
                    #     inlet_chn_3 = StreamInlet(one_stream)

            # add code maxSize 
            self.samples_chn_0 = np.array([])
            # self.samples_chn_1 = np.array([])
            # self.samples_chn_2 = np.array([])
            # self.samples_chn_3 = np.array([])


            # Initialize inlet 4 chn
            # inlet_chn_0 = StreamInlet(streams[0])
            # inlet_chn_1 = StreamInlet(streams[1])
            # inlet_chn_2 = StreamInlet(streams[2])
            # inlet_chn_3 = StreamInlet(streams[3])

            chunk_size = 1024
            # while count < (2):  
            # while count < (SAMPLING_FREQ * SHIFTED_DURATION):  # This code pull 4096 samples from LSL 
            # while count < (SAMPLING_FREQ * SHIFTED_DURATION/2):  # This code pull 2048 samples from LSL 
            count_sample = 0
            countty = 0
            
            while count_sample < (SAMPLING_FREQ * SHIFTED_DURATION/4):  # This code pull 1024 samples from LSL 
                for info in all_streams_name: # What is this line do?
                    self.sub_samples_chn_0, timestamps = inlet_chn_0.pull_sample()
                    # print(f"Sub Samples is: {self.sub_samples_chn_0[0]}")
                    # self.sub_samples_chn_1, timestamps = inlet_chn_1.pull_sample()
                    # self.sub_samples_chn_2, timestamps = inlet_chn_2.pull_sample()
                    # self.sub_samples_chn_3, timestamps = inlet_chn_3.pull_sample()

                    # Discuss with Pim: Can't use chunk --> difficulty in UI 
                    # self.sub_samples_chn_0, timestamps = inlet_chn_0.pull_chunk(max_samples=chunk_size)
                    
                    if timestamps:
                        # np.set_printoptions(threshold=np.inf)
                        self.samples_chn_0 = np.hstack((self.samples_chn_0, np.round(self.sub_samples_chn_0[0],7)))
                        # self.samples_chn_1 = np.hstack((self.samples_chn_1, np.round(self.sub_samples_chn_1[0],7)))
                        # self.samples_chn_2 = np.hstack((self.samples_chn_2, np.round(self.sub_samples_chn_2[0],7)))
                        # self.samples_chn_3 = np.hstack((self.samples_chn_3, np.round(self.sub_samples_chn_3[0],7)))

                    # self.samples_chn_0 = np.hstack((self.samples_chn_0, np.round(self.chunk[0], 7)))
                    # if len(self.samples_chn_0) == chunk_size:
                    #     break
                count_sample = count_sample + 1
                # time.sleep(0.0004)

            # #--------------------------------------------#
            filename = "inlet_pull_" + str(self.count_file)
            np.savetxt(filename, self.samples_chn_0)
            self.count_file += 1
            # #--------------------------------------------#



            print(f"Channel 0 inlet: {self.samples_chn_0}")
            # logging.info(f"Channel 1: {self.samples_chn_1}")
            # logging.info(f"Channel 2: {self.samples_chn_2}")
            # logging.info(f"Channel 3: {self.samples_chn_3}")

            print(f"Data size from Channel 0 is: {self.samples_chn_0.shape}")
            # print(f"Data size from Channel 1 is: {self.samples_chn_1.shape}")
            # print(f"Data size from Channel 2 is: {self.samples_chn_2.shape}")
            # print(f"Data size from Channel 3 is: {self.samples_chn_3.shape}")

            sys.stdout.flush()

            # Put those 4 in queue
            self.queue.put(self.samples_chn_0)
            # self.queue.put(self.samples_chn_1)
            # self.queue.put(self.samples_chn_2)
            # self.queue.put(self.samples_chn_3)

            self.put_flag.set()
            time.sleep(1)


    def send_data(self):
        self.channel_0_roll = np.zeros(2048)
        # self.channel_1_roll = np.zeros(2048)
        # self.channel_2_roll = np.zeros(2048)
        # self.channel_3_roll = np.zeros(2048)

        # self.roll_flag.set()
        while True:
            if not self.queue.empty():
                self.samples_chn_0 = self.queue.get()
                # self.samples_chn_1 = self.queue.get()
                # self.samples_chn_2 = self.queue.get()
                # self.samples_chn_3 = self.queue.get()

                # print(f"Channel 0 data is : {self.samples_chn_0}")
                # print(f"Channel 1 data is : {self.samples_chn_1}")
                # print(f"Channel 2 data is : {self.samples_chn_2}")
                # print(f"Channel 3 data is : {self.samples_chn_3}")

                print(f"Data size is:{self.samples_chn_0.shape}") # Should be 1024 samples
                # print(f"Data size is:{self.samples_chn_1.shape}") # Should be 1024 samples
                # print(f"Data size is:{self.samples_chn_2.shape}") # Should be 1024 samples
                # print(f"Data size is:{self.samples_chn_3.shape}") # Should be 1024 samples

                # while count_for_roll < 4:
                # while count_for_roll < (SAMPLING_FREQ * SHIFTED_DURATION): # This line should get 2048 samples
                # count_for_roll = 0
                # while count_for_roll < ((SAMPLING_FREQ * SHIFTED_DURATION)): # This line should get 1024 samples: get 1024 samples
                # while self.roll_flag.is_set(): # True = Flag
                # print(f"Sample shape Fp2 F8 is {self.samples_chn_0.shape}")

                self.channel_0_roll = np.roll(self.channel_0_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                self.channel_0_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.samples_chn_0

                # self.channel_1_roll = np.roll(self.channel_1_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                # self.channel_1_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.samples_chn_1

                # self.channel_2_roll = np.roll(self.channel_2_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                # self.channel_2_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.samples_chn_2

                # self.channel_3_roll = np.roll(self.channel_3_roll, SAMPLING_FREQ*SHIFTED_DURATION)
                # self.channel_3_roll[SAMPLING_FREQ*SHIFTED_DURATION:] = self.samples_chn_3

                print(f"Channel 0 After roll :{self.channel_0_roll}")
                print(f"Size: :{self.channel_0_roll.shape}")
                # print(f"Channel 1 After roll :{self.channel_1_roll}")
                # print(f"Size: :{self.channel_1_roll.shape}")
                # print(f"Channel 2 After roll :{self.channel_2_roll}")
                # print(f"Size: :{self.channel_2_roll.shape}")
                # print(f"Channel 3 After roll :{self.channel_3_roll}")
                # print(f"Size: :{self.channel_3_roll.shape}")

                sys.stdout.flush()
                self.queue2.put(self.channel_0_roll)
                # self.queue2.put(self.channel_1_roll)
                # self.queue2.put(self.channel_2_roll)
                # self.queue2.put(self.channel_3_roll)
    
                # self.put_flag.clear()
                # self.roll_flag.clear()
                time.sleep(1)