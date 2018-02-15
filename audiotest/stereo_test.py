from pyo import *

s = Server(nchnls=4, buffersize=1024, duplex=1)
s.setInOutDevice(5)
s.boot()

sound1 = "../Samples/flute.aif"
#sound1 = "../Samples/kick.wav"
sound2 = "../Samples/snare.wav"


#sfL = SfPlayer(sound1, loop=True, speed=0.2, mul=0.2).out()
sfL = SfPlayer(sound1, loop=True, speed=1.5, mul=0.2).mix(1).out()
#sdL = SmoothDelay(sfL.mix(4), delay=0.5, feedback=0.8, crossfade=0.05, mul=0.5).out(chnl=0, inc=2)

#sfR = SfPlayer(sound2, loop=True, speed=0.2, mul=0.2).out()
sfR = SfPlayer(sound2, loop=True, speed=0.5, mul=0.2).mix(2).out()
#sdR = SmoothDelay(sfR.mix(4), delay=0.5, feedback=0.5, crossfade=0.05, mul=0.5).out(chnl=1, inc=2)

#s.start()
s.gui(locals())

