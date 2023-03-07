import numpy as np
import time
import pylsl
import sys
from typing import List
from pylsl import StreamInlet, resolve_stream

SAMPLING_FREQ = 256
WINDOW_LENGTH = 8   # sec
NUM_BANDS = 8
OVERLAP_PERCENT = 0.5
SHIFTED_DURATION = 256  # 1024

class ReceiveData():
      
    Fp2_F8_data = np.zeros((8),dtype='float64')  
    F8_T8_data = np.zeros((8),dtype='float64')

    def __init__(self,sample_Fp2_F8,sample_F8_T8):
        self.sample_Fp2_F8 = sample_Fp2_F8
        self.sample_F8_T8 = sample_F8_T8

    def data_from_lsl(self):
        # self.sample_Fp2_F8 = np.array([])
        # self.sample_F8_T8 = np.array([])
        # streams = resolve_stream()

        # inlet_Fp2_F8 = StreamInlet(streams[0])
        # inlet_F8_T8 = StreamInlet(streams[1])
        # info = pylsl.StreamInfo()

        # count = 0

        # while count<(256):  
        #     for info in streams:
        #         self.sample_in_Fp2_F8, timestamps = inlet_Fp2_F8.pull_sample()
        #         self.sample_Fp2_F8 = np.hstack((self.sample_Fp2_F8,np.round(self.sample_in_Fp2_F8[0],7)))
    
        #         self.sample_in_F8_T8, timestamps = inlet_F8_T8.pull_sample()
        #         self.sample_F8_T8 = np.hstack((self.sample_F8_T8,np.round(self.sample_in_F8_T8[0],7)))

        #     time.sleep(0.0004)
        #     count += 1

        self.sample_Fp2_F8 = np.ones(1)
        self.sample_F8_T8 = np.ones(1)
        return self.sample_Fp2_F8,self.sample_F8_T8

    def roll_data(self):
        count = 0
        while count < 4:
            self.Fp2_F8_roll = np.roll(self.Fp2_F8_data, 1)
            self.F8_T8_roll = np.roll(self.F8_T8_data, 1)

            self.Fp2_F8_roll[:1] = self.sample_Fp2_F8
            self.F8_T8_roll[:1] = self.sample_F8_T8

            self.Fp2_F8_data = self.Fp2_F8_roll
            self.F8_T8_data = self.F8_T8_roll
            count += 1
        # count = 0
        var = self.Fp2_F8_data
        return var

if __name__ == '__main__':
    a = ReceiveData(np.array([]),np.array([]))   # new 4 sec data each channel
    while True:
        a.data_from_lsl()
        a.roll_data()
        sys.stdout.flush()