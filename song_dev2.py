from pyo import *
from random import shuffle, random
import sys
from system.controller import *
from time import sleep
import os


s = Server(nchnls=2, buffersize=1024, duplex=1)
s.setInOutDevice(2)
s.boot()
s.setStartOffset(0)
s.amp = 0.6


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

#Synth:
f = s.getSamplingRate() / 262144
t = PadSynthTable(basefreq=midiToHz(48), spread=1.205, bw=10, bwscl=1.5)
synth = Osc(table=t, freq=f, phase=[0, 0.5], mul=0.1).out(chnl=0, inc=1)
t2 = PadSynthTable(basefreq=midiToHz(48), spread=1.205, bw=10, bwscl=1.5)
synth2 = Osc(table=t, freq=f, phase=[0, 0.5], mul=0.4).out(chnl=0, inc=1)


#Krautbeat:
krautbeat = Seq(time=0.6,seq=[2,2,2,2,8],poly=1)
#krautbeat = Seq(time=0.6,seq=[2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,3,2,2,2,2,2,1,1,1,6],poly=1)
krauttable = LinTable([(0,0.0000),(6,0.8325),(236,0.0000),(1417,0.0000),(8192,0.0000)])
krautenv = TrigEnv(krautbeat, table=krauttable, dur=1.5, mul=0.7).mix(1)
krautgen = PinkNoise()
krautfiltfreq = LFO(freq=1,type=6, mul=0.3, add=3500.7)
krautfilt = Biquad(krautgen, freq=krautfiltfreq, q=5, type=0, mul=krautenv)
krautfiltpan = SPan(krautfilt, pan=0.3)
krautdelmul = LFO(freq=2,type=6, mul=1)
krautdel = Delay(krautfilt,delay=0.751,feedback=0.5, mul=krautdelmul)
krautdelpan = SPan(krautdel, pan=0.7)
krautrevinput = krautdelpan+krautfiltpan
krautrev = WGVerb(krautrevinput, feedback=0.9, bal=0.03)

#BASS
selbass = Beat(time=0.3, taps=5, w1=90, w2=54, w3=37, poly=4)
beat1 = [5, 1, 1, 1, 1, 0]
beat2 = [5, 1, 0, 1, 1, 1]
beat3 = [5, 1, 0, 1, 1, 0]
beat4 = [5, 1, 1, 0, 1, 0]
selbass.setPresets([beat1,beat2,beat3,beat4])
selbass.recall(0)
selbassm = selbass.mix(1)
bass_scale = [38, 38, 41, 41, 45, 45, 48, 48, 52, 52, 55, 55]
shuffle(bass_scale)
shuffledbassscale = DataTable(size=len(bass_scale),init=[midiToHz(i) for i in bass_scale])
basscount = Counter(selbassm,min=0,max=len(bass_scale))
basspitch = TableIndex(shuffledbassscale, basscount)
bassmul = TrigLinseg(selbass,list=[(0,0.0000),(0.01,0.3),(0.5,0)],mul=selbass['amp']).mix(1)
bass = SineLoop([basspitch, basspitch/2], feedback=0.1, mul=bassmul*0.4).mix(1).mix(2)

#Guitar:
g = Input(chnl=0)
g_rev = WGVerb(g, feedback=1, cutoff=5000, bal=.25, mul=0.8).out(chnl=1, inc=1)
g_del = SmoothDelay(g, delay=.6, feedback=.8, mul=0.5).out(chnl=0, inc=2)

def dsp_control():
    switch = read_digital(2)
    poti1 = read_poti(2, 5)
    poti2 = read_poti(3, 5)
    poti3 = read_poti(4, 5)
    poti4 = read_poti(5, 5)
    #Effects:
    val_poti1 = float(poti1) / 100
    val_poti2 = float(poti2) / 100
    val_poti3 = float(poti3) / 100
    val_poti4 = float(poti4) / 100
    synth.setFreq(f*val_poti1)
    synth2.setFreq(f*val_poti2)
    if switch is False:
        s.stop()

temps = -1
def timecontrol():
    global temps
    temps += 1
    print(temps)
    if temps == 0:
        dsp_control()
        krautbeat.play()
        krautrev.out()
        selbass.play()
        bass.out()
        g_rev.out()
    elif temps == 10:
        dsp_control()
    elif temps == 20:
        dsp_control()
    elif temps == 40:
        dsp_control()
    elif temps == 60:
        selbass.recall(1)
        dsp_control()
    elif temps == 120:
        selbass.recall(2)
        dsp_control()
    elif temps == 140:
        selbass.recall(3)
        dsp_control()
    elif temps == 150:
        krautbeat.stop()
        selbass.stop()
    elif temps == 151:
        dsp_control()
    elif temps == 152:
        dsp_control()
    elif temps == 154:
        dsp_control()
    elif temps == 156:
        dsp_control()
    else:
        pass

        
mainp = Pattern(timecontrol, 1)
mainp.play()

s.start()
