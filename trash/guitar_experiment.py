from pyo import *
from time import sleep

s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)
s.setInOutDevice(2)
s.boot()

s.start()
tab = NewTable(1)
rec = TableRec(Input(), tab)

env = HannTable()
pos = Randi(min=0, max=0.5, freq=[0.25, 0.3], mul=0.2)
dns = Randi(min=10, max=30, freq=.1)
pit = Randi(min=0.99, max=1.01, freq=100)
grn = Granule(tab, env, dens=30, pitch=0.8, pos=0, dur=1, mul=.1).mix(4).out()

while True:
    sleep(0.5)
    rec.play()
