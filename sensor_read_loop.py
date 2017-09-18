from controller import *
from pyo import *
from time import sleep
import subprocess
import time

#just for audiotest
pipe = subprocess.Popen(["python -i play_snd.py"], shell=True, stdin=subprocess.PIPE).stdin
time.sleep(2)

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
        while switch is True:
            switch = read_digital(2)
            sdown1 = 0
            sdown2 = 0
            lschuh = read_shoe(1, 20)
            rschuh = read_shoe(0, 20)
            poti1 = read_poti(2, 5)
            poti2 = read_poti(3, 5)
            poti3 = read_poti(4, 5)
            poti4 = read_poti(5, 5)
        #Trigger linker SCHUH
            if((lschuh == 1) and (trigger2 == 0)):
                trigger2 = 1
                sdown2 = 1
            if sdown2 == 1:
                snd = "./Samples/test.aiff"
                pipe.write("a.path = './Samples/kick.wav'\ndump = a.play()\n")
                #pipe.write("d.feedback = 1\ndump = a.play()\n")
            elif((lschuh == 0) and (trigger2 == 1)):
                trigger2 = 0
        #Trigger rechter SCHUH
            if((rschuh == 1) and (trigger1 == 0)):
                trigger1 = 1
                sdown1 = 1
            if sdown1 == 1:
                snd = "./Samples/kick.wav"
                test = float(poti2)/100
                pipe.write("a.path = './Samples/kick.wav'\ndump = a.play()\n")
            elif((rschuh == 0) and (trigger1 == 1)):
                trigger1 = 0




# Stop the audio Server before exiting
pipe.write("s.stop()\ntime.sleep(0.25)\n")
pipe.close()