import numpy as np
import time
import math

import pylsl
import pyqtgraph as pg
from typing import List
from pylsl import StreamInlet, resolve_stream


SAMPLING_FREQ = 256
WINDOW_LENGTH = 8
OVERLAP_PERCENT = 0.5
SHIFTED_DURATION = 4

class Test():
    
    Fp2_F8_data = np.array([0, 1, 2, 3, 4, 5, 6, 7],dtype='float64')  # 8 = SAMPLING_FREQ * WINDOW_LENGTH
    F8_T8_data = np.array([0, 1, 2, 3, 4, 5, 6, 7],dtype='float64')

    def __init__(self,sample_Fp2_F8,sample_F8_T8):
        self.sample_Fp2_F8 = sample_Fp2_F8
        self.sample_F8_T8 = sample_F8_T8

    def main(self):
        self.sample_Fp2_F8 = np.array([])
        self.sample_F8_T8 = np.array([])
        # first resolve an EEG stream on the lab network
        streams = resolve_stream()


        # create a new inlet to read from the stream
        inlet_Fp2_F8 = StreamInlet(streams[0])
        inlet_F8_T8 = StreamInlet(streams[1])
        info = pylsl.StreamInfo()

        count = 0

        while count<2: 
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            for info in streams:
                self.sample_in_Fp2_F8, timestamps = inlet_Fp2_F8.pull_sample()
                self.sample_Fp2_F8 = np.hstack((self.sample_Fp2_F8,np.round(self.sample_in_Fp2_F8[0],7)))
    
                self.sample_in_F8_T8, timestamps = inlet_F8_T8.pull_sample()
                self.sample_F8_T8 = np.hstack((self.sample_F8_T8,np.round(self.sample_in_F8_T8[0],7)))

            time.sleep(0.0004)
            count += 1
        print(f'sample0: {self.sample_Fp2_F8}')
        print(f'sample1: {self.sample_F8_T8}')

        return self.sample_Fp2_F8,self.sample_F8_T8

    def data_slicing(self):
        
        self.Fp2_F8_roll = np.roll(self.Fp2_F8_data, SHIFTED_DURATION)
        self.F8_T8_roll = np.roll(self.F8_T8_data, SHIFTED_DURATION)

        self.Fp2_F8_roll[-SHIFTED_DURATION:] = self.sample_Fp2_F8
        self.F8_T8_roll[-SHIFTED_DURATION:] = self.sample_F8_T8

        self.Fp2_F8_data = self.Fp2_F8_roll
        self.F8_T8_data = self.F8_T8_roll

        print(self.Fp2_F8_data)
        print(self.F8_T8_data)


if __name__ == '__main__':
    a = Test(np.array([]),np.array([]))   # new 4 sec data each channel
    while True:
        a.main()
        a.data_slicing()





    