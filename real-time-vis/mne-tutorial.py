# from youtube
import mne
import matplotlib.pyplot as plt

path = r'../dataset/chb15/chb15_06.edf'
raw = mne.io.read_raw_edf(path, preload=True)

# raw.filter(1, 20)
# raw.plot()

# read = mne.read_events(raw, return_event_id=True)
# print(read)


def read_data(path):
    data = mne.io.read_raw_edf(path, preload=True)
    data.set_eeg_reference()
    data.filter(l_freq=1, h_freq=20)
    epochs = mne.make_fixed_length_epochs(data, duration=5, overlap=1)
    array = epochs.get_data()
    return array


sample_data = read_data(path)
print(sample_data.shape)  # no. epochs, channels, length of signal

event = mne.find_events(raw)
print("There are ", event)

event_ids = {
    "nonseizure": 545,
    "seizure": 184
}
epochs = mne.Epochs(raw, events, event_id=event_ids)

epochs.plot()

# plt.show()
