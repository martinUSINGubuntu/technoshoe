from pyo import *
from controller import *
from time import sleep

s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)
s.setInOutDevice(2)
s.boot()


a = Sine(440, 0, 0.1).out()
b = Sine(440, 0, 0.1).out()
d1 = Delay(a, delay=0.0, feedback=0.0, mul=.4).out()
d2 = Delay(b, delay=0.0, feedback=0.0, mul=.4).out()


#initialize serial reading
rschuh = serial_init(0)
lschuh = serial_init(1)
poti1 = serial_init(2)
poti2 = serial_init(3)
poti3 = serial_init(4)
poti4 = serial_init(5)

#initialize digital reading
switch = read_digital(2)
sleep(0.5)

switch = read_digital(2)
print(switch)
while True:
    switch = read_digital(2)
    if switch is True:
        s.start()
        while switch is True:
            switch = read_digital(2)
            poti1 = read_poti(2, 5)
            poti2 = read_poti(3, 5)
            poti3 = read_poti(4, 5)
            poti4 = read_poti(5, 5)
            freq1 = poti1* 5 + 300
            freq2 = poti2* 5 + 300
            a.setFreq(freq1)
            b.setFreq(freq2)
            _feedback_poti3 = float(poti3) / 100
            _feedback_poti4 = float(poti4) / 100
            d1.setDelay(_feedback_poti3)
            d2.setFeedback(_feedback_poti4)
    if switch is False:
        s.stop()