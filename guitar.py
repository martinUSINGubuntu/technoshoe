from pyo import *
from time import sleep

s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)
s.setInOutDevice(9)
s.boot()

s.start()
tab = NewTable(16)
rec = TableRec(Input(), tab)

pit = Choice(choice=[.8, .4], freq=[3])
dur = Choice(choice=[0.4, 0.8], freq=4)
a = Looper(table=tab,pitch=0.8,start=0,dur=2,mode=1,startfromloop=True,mul=0.25).out(chnl=1)

while True:
    sleep(2)
    rec.play()

#s.gui(locals())