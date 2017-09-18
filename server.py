from pyo import *

class Audio:
    def __init__(self):
        s = Server(duplex=0).boot()
        s.start()

    def chorus(self, _sample, _feedback):
        a = SfPlayer(_sample)
        d = Delay(a, delay=[0.1, 0.2], feedback=_feedback, mul=0.4).out()
        d.mix(2).out()




