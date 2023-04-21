import numpy as np
import wavio

rate = 22050           # samples per second
T = 3                  # sample duration (seconds)
n = int(rate*T)        # number of samples
t = np.arange(n)/rate  # grid of time values

f = 440.0              # sound frequency (Hz)
x = np.sin(2*np.pi * f * t)

print(x)
wavio.write("sine24.wav", x, rate, sampwidth=3)