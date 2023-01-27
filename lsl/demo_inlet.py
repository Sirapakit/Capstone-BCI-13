import numpy as np
import math
import pylsl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
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

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        sample_filter = filter(sample)
        print(f'sample:{sample}')
        print(f'signal:{sample_filter}')
        # print(timestamp, sample)

if __name__ == '__main__':
    main()





    