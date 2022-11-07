import sys
import getopt
import time
from random import random as rand
from pylsl import StreamInfo, StreamOutlet, local_clock
import numpy as np
from numpy import loadtxt

# data = open('chb01_26.csv')
#data = csv.reader(file)
# file = "chb01_26.edf"
# data = mne.io.read_raw_edf(file)
# test = np.load('data_ten.npy').tolist()
test = np.load('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\data_15.npy')
# test10 = test * 10
test_T = np.transpose(test)
test_L = test_T.tolist()
# F8_T9_channel = test_L[:]
# print(F8_T9_channel)
#raw_data = data.get_data()
#info = data.info
# channels = data.ch_names
# raw_pick_channels = data.pick_channels(['F8-T8']).get_data().tolist()
# raw_pick_channels_0 = raw_pick_channels[0]
# print(type(raw_pick_channels))
# print(raw_pick_channels[0][:23])

def main(argv):
    srate = 256
    name = 'BioSemi'
    type = 'EEG'
    n_channels = 1
    help_string = 'SendData.py -s <sampling_rate> -n <stream_name> -t <stream_type>'
    try:
        opts, args = getopt.getopt(argv, "hs:c:n:t:", longopts=["srate=", "channels=", "name=", "type"])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-s", "--srate"):
            srate = float(arg)
        elif opt in ("-c", "--channels"):
            n_channels = int(arg)
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-t", "--type"):
            type = arg

    info = StreamInfo(name, type, n_channels, srate, 'float32', 'myuid34234')

    # next make an outlet
    outlet = StreamOutlet(info)

    print("now sending data...")
    start_time = local_clock()
    sent_samples = 0
    
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
            mysample =  [test_L[sent_samples][i] for i in range(n_channels)]
                # print(mysample)
                # [rand() for _ in range(n_channels)]
                # [raw_pick_channels_0[i] for i in range(n_channels)]
                # [F8_T9_channel[i] for i in range(n_channels)]
            outlet.push_sample(mysample)
            print(mysample)
        sent_samples += required_samples
        time.sleep(0.0004)

if __name__ == '__main__':
    main(sys.argv[1:])