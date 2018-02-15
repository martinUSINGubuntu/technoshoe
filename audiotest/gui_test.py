from pyo import *
from time import sleep


s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)

s.setInOutDevice(2)
s.boot()
s.amp = 0.1

# Creates two objects with cool parameters, one per channel.
a = Sine(440, 0, 0.1).out()
d1 = Delay(a, delay=0.0, feedback=0.0, mul=.4).out()
b = FM().out(1)

# Opens the controller windows.
a.ctrl(title="Sinus left channel")
d1.ctrl(title="Delay sinus")
b.ctrl(title="Frequency modulation right channel")
sc = Scope([a, d1, b])


s.gui(locals())