import sys
import getopt
import time
from pylsl import StreamInfo, StreamOutlet, local_clock
import numpy as np
from numpy import loadtxt

database = np.load('./chb05-2chn.npy')
database_list = database.tolist()
all_channel_name = 2

def main(argv):
    srate = 256
    name_Fp2_F8 = 'Fp2-F8'
    name_F8_T8 = 'F8-T8'
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

    info_Fp2_F8 = StreamInfo(name_Fp2_F8, type, n_channels, srate, 'float32', 'myuid34234')
    info_F8_T8 = StreamInfo(name_F8_T8, type, n_channels, srate, 'float32', 'myuid34234')

    # # next make an outlet
    outlet_Fp2_F8 = StreamOutlet(info_Fp2_F8)
    outlet_F8_T8 = StreamOutlet(info_F8_T8)
    # outlet = StreamOutlet(info)
    print("now sending data...")
    start_time = local_clock()
    sent_samples = 0
    
    while True:
        elapsed_time = local_clock() - start_time
        required_samples = int(srate * elapsed_time) - sent_samples
        for sample_ix in range(required_samples):
            mysample =  [database_list[sent_samples][i] for i in range(all_channel_name)]
            # print(mysample)

            mysample_Fp2_F8_list = [float(mysample[0])]
            mysample_F8_T8_list = [float(mysample[1])]
            # mysample_Fp2_F8_list = [0]
            # mysample_F8_T8_list = [1]

            # print(f'mysample[0]: {mysample_Fp2_F8_list}')
            # print(f'mysample[1]: {mysample_F8_T8_list}')

            outlet_Fp2_F8.push_sample(mysample_Fp2_F8_list)
            outlet_F8_T8.push_sample(mysample_F8_T8_list)

        sent_samples += required_samples
        time.sleep(0.0004)

if __name__ == '__main__':
    main(sys.argv[1:])