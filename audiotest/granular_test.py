from pyo import *
from time import sleep

s = Server(nchnls=2, buffersize=1024, duplex=1)
s.setInOutDevice(5)
s.boot()

snd = SndTable("../Samples/snare.wav")
env = HannTable()
pos = Phasor(freq=snd.getRate()*.25, mul=snd.getSize())
dur = Noise(mul=.001, add=.1)
g = Granulator(snd, env, [1, 1.001], pos, dur, 32, mul=0.05).out()

s.gui(locals())