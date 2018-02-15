from pyo import *
from time import sleep
import os

# Audio inputs must be available.
s = Server(sr=44100, nchnls=4, buffersize=1024, duplex=1)
s.setInOutDevice(2)
s.boot()
s.start()

# Path of the recorded sound file.
path = os.path.join(os.path.expanduser("~"), "Desktop", "synth.wav")

# Creates a two seconds stereo empty table. The "feedback" argument
# is the amount of old data to mix with a new recording (overdub).
t = NewTable(length=4, chnls=4, feedback=0.2)

# Retrieves the stereo input
inp = Input(0)

# Table recorder. Call rec.play() to start a recording, it stops
# when the table is full. Call it multiple times to overdub.
rec = TableRec(inp, table=t, fadetime=0.05)

# Reads the content of the table in loop.
osc = Osc(table=t, freq=t.getRate(), mul=0.4)
revr = WGVerb(osc.mix(), feedback=0.9, cutoff=5000, bal=.25, mul=.2).out(chnl=1, inc=2)

while True:
    rec.play()
    sleep(20)