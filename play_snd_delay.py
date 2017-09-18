#!/usr/bin/env python
# encoding: utf-8
"""
Simple soundfile player used by 06_separated_threads.py example.

"""
from pyo import *

s = Server()
s.setInOutDevice(2)
s.boot()

#a = SfPlayer('./Samples/snd_2.aif')
a = SfPlayer('./Samples/test.aiff')
d = Delay(a, delay=[.1,.2], feedback=.5, mul=.4).out()
a2 = d.mix(2).out()


s.start()
