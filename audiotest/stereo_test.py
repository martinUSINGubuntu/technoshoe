from pyo import *

s = Server(nchnls=4, buffersize=1024, duplex=1)
s.setInOutDevice(2)
s.boot()

sound1 = "../Samples/kick.wav"
sound2 = "../Samples/snare.wav"


sfL = SfPlayer(sound1, loop=True, speed=1.5, mul=0.2).mix(1).out()

sfR = SfPlayer(sound2, loop=True, speed=0.5, mul=0.2).mix(2).out()

s.gui(locals())

