import sys
import getopt
import time
from pylsl import StreamInfo, StreamOutlet, local_clock
import numpy as np
from numpy import loadtxt

database = np.load('./chb03-4chn-for-stream.npy')
database = np.transpose(database)
database_list = database.tolist()
all_channel_name = 4

def main(argv):
    srate = 256
    name_bipolar_ch1 = 'bipolar_ch1_database'
    name_bipolar_ch2 = 'bipolar_ch2_database'
    name_bipolar_ch3 = 'bipolar_ch3_database'
    name_bipolar_ch4 = 'bipolar_ch4_database'
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
    
    print('ok')
    info_bipolar_ch1 = StreamInfo(name_bipolar_ch1, type, n_channels, srate, 'float32', 'myuid34234')
    info_bipolar_ch2 = StreamInfo(name_bipolar_ch2, type, n_channels, srate, 'float32', 'myuid34234')
    info_bipolar_ch3 = StreamInfo(name_bipolar_ch3, type, n_channels, srate, 'float32', 'myuid34234')
    info_bipolar_ch4 = StreamInfo(name_bipolar_ch4, type, n_channels, srate, 'float32', 'myuid34234')

    outlet_bipolar_ch1 = StreamOutlet(info_bipolar_ch1)
    outlet_bipolar_ch2 = StreamOutlet(info_bipolar_ch2)
    outlet_bipolar_ch3 = StreamOutlet(info_bipolar_ch3)
    outlet_bipolar_ch4 = StreamOutlet(info_bipolar_ch4)

    print("now sending data...")
    start_time = local_clock()
    sent_samples = 0
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
            streamed_sample =  [database_list[sent_samples][i] for i in range(all_channel_name)]

            sample_bipolar_ch1_list = [float(streamed_sample[0])]
            sample_bipolar_ch2_list = [float(streamed_sample[1])]
            sample_bipolar_ch3_list = [float(streamed_sample[2])]
            sample_bipolar_ch4_list = [float(streamed_sample[3])]

            outlet_bipolar_ch1.push_sample(sample_bipolar_ch1_list)
            outlet_bipolar_ch2.push_sample(sample_bipolar_ch2_list)
            outlet_bipolar_ch3.push_sample(sample_bipolar_ch3_list)
            outlet_bipolar_ch4.push_sample(sample_bipolar_ch4_list)

        sent_samples += required_samples
        time.sleep(0.0004)

if __name__ =='__main__':
    main(sys.argv[1:])