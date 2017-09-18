##!/usr/bin/env python
## encoding: utf-8
#"""
#Simple soundfile player used by 06_separated_threads.py example.

#"""
#from pyo import *

#s = Server(duplex=0).boot()

#a = SfPlayer('./Samples/test.aiff')
#a.mix(2).out()


#s.start()

#!/usr/bin/env python
# encoding: utf-8
"""
Simple soundfile player used by 06_separated_threads.py example.

"""
from pyo import *

s = Server()
s.setInOutDevice(2)
s.boot()

a = SfPlayer('./Samples/kick.wav')
#chor = Chorus(a, depth=[1.1,1.9], feedback=0.5, bal=0.5).out()
chor = Chorus(a, depth=[1.1,1.9], bal=0.5).out()
a2 = chor.mix(2).out()


s.start()