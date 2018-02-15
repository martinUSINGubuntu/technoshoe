from pyo import *

s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)
s.setInOutDevice(2)
s.boot()

sound1 = "../Samples/kick.wav"
sound2 = "../Samples/snare.wav"

t1 = SndTable(sound1)
freq1 = t1.getRate()
osc = Osc(table=t1, freq=freq1, phase=[0.5, 0.2], mul=0.3).out()

t2 = SndTable(sound2)
freq2 = t2.getRate()
osc2 = Osc(table=t2, freq=freq2, mul=0.3).out()

#sfL = SfPlayer(sound1, loop=True, speed=1, mul=0.5).out()
#sfR = SfPlayer(sound2, loop=True, speed=1, mul=0.5).out(1)

s.gui(locals())