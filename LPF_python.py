'''
Created on 10 de nov de 2017

@author: pyetr_a1q8rre
'''
import struct
import wave
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import scipy

# define stream chunk
chunk = 20 * 4096

# open a wav format music
f = wave.open("Daft_Punk_Get_Lucky.wav", "rb")

# instantiate PyAudio
p = pyaudio.PyAudio()
formato = p.get_format_from_width(f.getsampwidth())
frame_rate = f.getframerate()

print('formato ', formato, 'width ', f.getsampwidth(), 'channels ', f.getnchannels())

# open stream
stream = p.open(format=formato,
                channels=f.getnchannels(),
                rate=frame_rate,
                output=True)

# read data
f.readframes(chunk)
data = f.readframes(chunk)

size = 2 * chunk - 1
fmt = str(size) + 'HH'

print('len(data)', len(data), "calcsize ", struct.calcsize(fmt))

data_ = np.reshape(np.fromstring(data, 'Int16'), [chunk, 2])
x = np.arange(len(data_[:, 0]))

plt.ion()


# START


def butter_filter(cutoff, frame_rate, order=5):
    nyq = frame_rate / 2
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data_, cutoff, frame_rate, order=5):
    b, a = butter_filter(cutoff, frame_rate, order=order)
    y = scipy.signal.lfilter(b, a, data_)
    return y

cutoff = 3.667       # cutoff frequency in rad/s
fs = 30.0     # imported frame rate
order = 6          # filter order

b, a = butter_filter(cutoff, fs, order)     # get the filter coefficients



# FINISH

# play stream
while data:
    data_ = np.reshape(np.fromstring(data, 'Int16'), [chunk, 2])

    plt.plot(data_[:, 0])

    plt.ylim((-40000, 40000))
    plt.draw()
    plt.pause(0.0000001)
    plt.gcf().clear()

    stream.write(data)
    data = f.readframes(chunk)

# stop stream
stream.stop_stream()
stream.close()

# close PyAudio
