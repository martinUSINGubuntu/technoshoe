from controller import *
from pyo import *
from time import sleep

s = Server()
s.setInOutDevice(2)
s.boot()

delaytime_poti1 = 0.0
delaytime_poti2 = 0.0
feedback_poti3 = 0.0
feedback_poti4 = 0.0

snd_r = "./Samples/snare.wav"
sr = SfPlayer(snd_r)
rev1 = WGVerb(sr, feedback=0.3, cutoff=5000, bal=.25, mul=.6).out()
#rev1 = Freeverb(sr, size=0.0, damp=0.5, bal=0.0).out()
#d2 = Delay(sr, delay=delaytime_poti2, feedback=feedback_poti4, mul=1).out()

snd_l = "./Samples/kick.wav"
sl = SfPlayer(snd_l)
#rev2 = Freeverb(sl, size=0.5, damp=0.5, bal=.5).out()
rev3 = WGVerb(sl, feedback=0.4, cutoff=5000, bal=.25, mul=.6).out()
#d1 = Delay(sl, delay=delaytime_poti1, feedback=feedback_poti3, mul=1).out()

#d1 = Delay(sample_r, delay=0.0, feedback=1, mul=.6).out()
#d2 = Delay(sample_l, delay=0.0, feedback=1, mul=.6).out()

#shoe state
trigger1 = 0
sdown1 = 0
trigger2 = 0
sdown2 = 0

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

while True:
    switch = read_digital(2)
    if switch is True:
        s.start()
        while switch is True:
        #Read all Sensors:
            switch = read_digital(2)
            sdown1 = 0
            sdown2 = 0
            lschuh = read_shoe(1, 20)
            rschuh = read_shoe(0, 40)
            poti1 = read_poti(2, 5)
            poti2 = read_poti(3, 5)
            poti3 = read_poti(4, 5)
            poti4 = read_poti(5, 5)
        #Effects:
            delaytime_poti1 = float(poti1) / 100
            delaytime_poti2 = float(poti2) / 100
            feedback_poti3 = float(poti3) / 100
            feedback_poti4 = float(poti4) / 100
            #d1.setFeedback(feedback_poti3)
            #d2.setFeedback(feedback_poti4)
            #d1.setDelay(delaytime_poti1)
            #d2.setDelay(delaytime_poti2)
        #Trigger linker SCHUH:
            if((lschuh == 1) and (trigger2 == 0)):
                trigger2 = 1
                sdown2 = 1
            if sdown2 == 1:
                sl.play()
            elif((lschuh == 0) and (trigger2 == 1)):
                trigger2 = 0
        #Trigger rechter SCHUH
            if((rschuh == 1) and (trigger1 == 0)):
                trigger1 = 1
                sdown1 = 1
            if sdown1 == 1:
                sr.play()
            elif((rschuh == 0) and (trigger1 == 1)):
                trigger1 = 0
    if switch is False:
        s.stop()
