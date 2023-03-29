import sys
import getopt
import time
from pylsl import StreamInfo, StreamOutlet, local_clock
import numpy as np

# define data to stream
database = np.load('../lsl/moke-1-100-data.npy')
num_samples = database.shape[1]
# database = np.transpose(database)
# database_list = database.tolist()

# define the stream properties
stream_name = "my_stream"
stream_type = "EEG"
num_channels = 4
sample_rate = 250
channel_format = "float32"
stream_id = "my_stream_id"
# stream_name = "my_stream"
# stream_id = "my_stream_id"

# create the stream info object
info = StreamInfo(stream_name, stream_type, num_channels, sample_rate, channel_format, stream_id)

# create the stream outlet object
outlet = StreamOutlet(info)

# loop data to stream
sent_samples = 0
while True:
    for i in range(num_samples):
        data = database[:, i]  # extract a single sample from the database
        outlet.push_sample(data.tolist())  # push the sample to the stream as a list
        time.sleep(1.0 / sample_rate)


        """
        # data = np.array([random.random() for i in range(num_channels)]) 
        data = np.array([database_list[sent_samples] for i in range(sample_rate)]) 
        outlet.push_sample(data)  # push the data to the stream
        
        time.sleep(1/sample_rate)  # wait for the sample rate
        """
        # # stream the data in real-time
        # for i in range(num_samples):
        #     data = database[:, i]  # extract a single sample from the database
        #     outlet.push_sample(data.tolist())  # push the sample to the stream as a list
        #     time.sleep(1.0 / sample_rate)