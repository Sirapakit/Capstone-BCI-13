import numpy as np
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
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    info = pylsl.StreamInfo()
    streams = pylsl.resolve_streams()

    sample_Fp2_F8 = []
    sample_F8_T8 = []
    count = 0
    while count < 10: 
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        for info in streams:
            if info.name() == 'Fp2-F8':
                sample_Fp2_F8.append(sample[0])
            if info.name() == 'F8-T8':
                sample_F8_T8.append(sample[0])
        count += 1
        # print(timestamp, sample)
    print(f'Fp2-F8: {sample_Fp2_F8}')
    print(f'F8-T8: {sample_F8_T8}')
if __name__ == '__main__':
    main()





    