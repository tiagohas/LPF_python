'''
Created on 10 de nov de 2017

@author: pyetr_a1q8rre
'''
import pyaudio
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np

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