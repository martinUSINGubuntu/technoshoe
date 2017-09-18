from controller import *
from pyo import *
from time import sleep


s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)
s.setInOutDevice(2)
s.boot()



tab = NewTable(4)
rec = TableRec(Input(), tab)


pit = Choice(choice=[5, 7], freq=[2])
#dur = Choice(choice=[.0625,.125,.125,.125,.25,.25,.5], freq=4)
dur = Choice(choice=[.125,.125,.2], freq=4)
a = Looper( table=tab, # table to loop in
            pitch=pit, # transposition
            start=0,
            #start=start, # loop start position
            dur=1,
            #dur=dur, # loop duration
            xfade=20, # crossfade duration in %
            mode=1, # looping mode
            xfadeshape=0, # crossfade shape
            startfromloop=False, # first start position, False means from beginning of the table
            interp=4, # interpolation method
            mul=0.3
            ).out(chnl=1)


delaytime_poti1 = 0.0
delaytime_poti2 = 0.0
feedback_poti3 = 0.0
feedback_poti4 = 0.0

snd_r = "./Samples/snare.wav"
sr = SfPlayer(snd_r)
sdr = SmoothDelay(sr, delay=0.2, feedback=0.5, crossfade=0.05, mul=0.3).out(chnl=3)
revr = WGVerb(sr, feedback=0.4, cutoff=5000, bal=.25, mul=.3).out(chnl=4)


snd_l = "./Samples/kick.wav"
sl = SfPlayer(snd_l)
sdl = SmoothDelay(sl, delay=0.2, feedback=0.5, crossfade=0.05, mul=0.3).out(chnl=3)
revl = WGVerb(sl, feedback=0.4, cutoff=5000, bal=.25, mul=.3).out(chnl=4)



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
x=1

while True:
    switch = read_digital(2)
    if switch is True:
        s.start()
        while switch is True:
        #Read all Sensors:
            sleep(0.1)
            x+=1
            if x == 20:
                rec.play()
                x = 1
                print("loop")
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
            val_poti1 = float(poti1) / 100
            val_poti2 = float(poti2) / 100
            val_poti3 = float(poti3) / 100
            val_poti4 = float(poti4) / 100
            sdl.setDelay(val_poti1)
            sdr.setDelay(val_poti2)
            revl.setFeedback(val_poti3)
            revr.setFeedback(val_poti4)
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
                #rec.play()
            elif((rschuh == 0) and (trigger1 == 1)):
                trigger1 = 0
    if switch is False:
        s.stop()
