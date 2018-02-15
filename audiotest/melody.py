from pyo import *
from controller import *
from time import sleep

def read_controller():
    switch = read_digital(2)
    if switch is True:
        switch = read_digital(2)
        poti1 = read_poti(2, 5)
        poti2 = read_poti(3, 5)
        poti3 = read_poti(4, 5)
        poti4 = read_poti(5, 5)
        freq1 = poti1* 5 + 300
        freq2 = poti2* 5 + 300
        #speed = float(poti1) / 100
        a.setFreq(freq1)
        #speed2 = float(poti2) / 100
        #sin2.setFreq(freq2)
        _feedback_poti3 = float(poti3) / 100
        _feedback_poti4 = float(poti4) / 100
        d1.setDelay(_feedback_poti3)
        #d2.setFeedback(_feedback_poti4)
    if switch is False:
        print("switch false")


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


#read_controller()
a.setFreq(200)

s.gui(locals())