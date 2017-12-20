from controller import *
from pyo import *
from time import sleep

def rundsp(file_l, file_r):
    s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)
    s.setInOutDevice(9)
    s.boot()

    snd_l = file_l
    sl = SfPlayer(snd_l)
    sdl = SmoothDelay(sl.mix(4), delay=0.2, feedback=0.5, crossfade=0.05, mul=0.2).out(chnl=0, inc=2)
    revl = WGVerb(sl.mix(4), feedback=0.4, cutoff=5000, bal=.25, mul=.2).out(chnl=0, inc=2)

    snd_r = file_r
    sr = SfPlayer(snd_r)
    sdr = SmoothDelay(sr.mix(4), delay=0.2, feedback=0.5, crossfade=0.05, mul=0.2).out(chnl=1, inc=2)
    revr = WGVerb(sr.mix(), feedback=0.4, cutoff=5000, bal=.25, mul=.2).out(chnl=1, inc=2)

    #initialize serial reading
    rschuh = serial_init(0)
    lschuh = serial_init(1)
    poti1 = serial_init(2)
    poti2 = serial_init(3)
    poti3 = serial_init(4)
    poti4 = serial_init(5)

    #initialize digital reading
    switch = read_digital(2)
    sleep(1)

    #initial shoe state
    trigger1 = 0
    sdown1 = 0
    trigger2 = 0
    sdown2 = 0

    while True:
        switch = read_digital(2)
        if switch is True:
            s.start()
        while switch is True:
            #Read all Sensors:
            sleep(0.02)
            switch = read_digital(2)
            sdown1 = 0
            sdown2 = 0
            lschuh = read_shoe(1, 40)
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
            elif ((rschuh == 0) and (trigger1 == 1)):
                trigger1 = 0
        if switch is False:
            s.stop()