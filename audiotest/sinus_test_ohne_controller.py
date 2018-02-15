from pyo import *
from random import randint
import time

s = Server(nchnls=4, buffersize=1024, duplex=1)
s.setInOutDevice(2)
s.boot()


a = Sine(440, 0, 0.2).out()

s.start()

for x in range(10):
    a.setFreq(randint(250,600))
    time.sleep(1)

s.stop()
s.shutdown()



