import sys
import getopt
import time
from pylsl import StreamInfo, StreamOutlet, local_clock
import numpy as np

# database = np.load('../lsl/chb03-8coeff.npy')
database = np.load('../lsl/chb17-8coeff.npy')
# database = np.load('../lsl/chb06-8coeff.npy')

# database = np.load('../lsl/moke-1-100-data.npy')
database = np.transpose(database)
all_channel_name = 4

def main(argv):
    srate = 256
    name = 'my_stream'
    type = 'EEG'
    n_channels = 4
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
    info = StreamInfo(name, type, n_channels, srate, 'float32', 'myuid34234')
    outlet = StreamOutlet(info)

    print("now sending data...")
    start_time = local_clock()

    sent_samples = 0
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
            streamed_sample =  [database[sent_samples][i] for i in range(all_channel_name)]
            outlet.push_sample(streamed_sample)

        sent_samples += required_samples
        time.sleep(0.0004)

if __name__ =='__main__':
    main(sys.argv[1:])
