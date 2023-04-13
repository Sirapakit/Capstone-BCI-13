import sys
import getopt
import time
from pylsl import StreamInfo, StreamOutlet, local_clock
import numpy as np

database = np.load('../lsl/chb03-8coeff.npy')
# database = np.load('../lsl/moke-1-100-data.npy')
database = np.transpose(database)
all_channel_name = 4

def main(argv):
    srate = 256
    name_queue = 'my_stream'
    name_bipolar_1 = 'bipolar_ch1_database'
    name_bipolar_2 = 'bipolar_ch2_database'
    name_bipolar_3 = 'bipolar_ch3_database'
    name_bipolar_4 = 'bipolar_ch4_database'
    type = 'EEG'
    n_channels_queue = 4
    n_channels_bipolar = 1
    help_string = 'SendData.py -s <sampling_rate> -n <stream_name> -t <stream_type>'
    try:
        opts, args = getopt.getopt(argv, "hs:n:t:", longopts=["srate=", "name=", "type"])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-s", "--srate"):
            srate = float(arg)
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-t", "--type"):
            type = arg
    
    print('ok')
    info_queue = StreamInfo(name_queue, type, n_channels_queue, srate, 'float32', 'myuid34234')
    info_bipolar_1 = StreamInfo(name_bipolar_1, type, n_channels_bipolar, srate, 'float32', 'myuid34234')
    info_bipolar_2 = StreamInfo(name_bipolar_2, type, n_channels_bipolar, srate, 'float32', 'myuid34234')
    info_bipolar_3 = StreamInfo(name_bipolar_3, type, n_channels_bipolar, srate, 'float32', 'myuid34234')
    info_bipolar_4 = StreamInfo(name_bipolar_4, type, n_channels_bipolar, srate, 'float32', 'myuid34234')

    outlet_queue = StreamOutlet(info_queue)
    outlet_bipolar_1 = StreamOutlet(info_bipolar_1)
    outlet_bipolar_2 = StreamOutlet(info_bipolar_2)
    outlet_bipolar_3 = StreamOutlet(info_bipolar_3)
    outlet_bipolar_4 = StreamOutlet(info_bipolar_4)

    print("now sending data...")
    start_time = local_clock()

    sent_samples = 0
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
            streamed_sample =  [database[sent_samples][i] for i in range(all_channel_name)]
            sample_bipolar_1 = [streamed_sample[0]]
            sample_bipolar_2 = [streamed_sample[1]]
            sample_bipolar_3 = [streamed_sample[2]]
            sample_bipolar_4 = [streamed_sample[3]]
            outlet_queue.push_sample(streamed_sample)
            outlet_bipolar_1.push_sample(sample_bipolar_1)
            outlet_bipolar_2.push_sample(sample_bipolar_2)
            outlet_bipolar_3.push_sample(sample_bipolar_3)
            outlet_bipolar_4.push_sample(sample_bipolar_4)
        sent_samples += required_samples
        time.sleep(0.0004)

if __name__ =='__main__':
    main(sys.argv[1:])
