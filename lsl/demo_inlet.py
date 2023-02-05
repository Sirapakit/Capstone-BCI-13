import numpy as np
import time
import math

import pylsl
import pyqtgraph as pg
from typing import List
from pylsl import StreamInlet, resolve_stream
# from joblib import load

def filter(sample_from_lsl):
    result = []
    for i in sample_from_lsl:
        result.append(i*2)
    return result

def main():
    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream()
    print(f'streams(20): {streams}')
    print(streams)

    # create a new inlet to read from the stream
    inlet_Fp2_F8 = StreamInlet(streams[0])
    inlet_F8_T8 = StreamInlet(streams[1])
    info = pylsl.StreamInfo()
    # streams = pylsl.resolve_streams()
    # print(f'streams(26): {streams}')

    sample_Fp2_F8 = []
    sample_F8_T8 = []
    count = 0

    while count<10: 
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        for info in streams:
            sample_in_Fp2_F8, timestamps = inlet_Fp2_F8.pull_sample()
            # print('Adding marker inlet: ' + info.name())
            sample_Fp2_F8.append(sample_in_Fp2_F8[0])
            sample_in_F8_T8, timestamps = inlet_F8_T8.pull_sample()
            # print('Adding marker inlet: ' + info.name())
            sample_F8_T8.append(sample_in_F8_T8[0])
        time.sleep(0.0004)
        count += 1
    print(f'sample0: {sample_Fp2_F8}')
    print(f'sample1: {sample_F8_T8}')

if __name__ == '__main__':
    main()





    