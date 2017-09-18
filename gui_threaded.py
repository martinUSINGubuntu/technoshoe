import threading
from Tkinter import *
import Tkinter as tk
from pyo import *
from glob import glob
from time import sleep
import sys
#from controller import *


class BackgroundTask():

    def __init__( self, taskFuncPointer ):
        self.__taskFuncPointer_ = taskFuncPointer
        self.__workerThread_ = None
        self.__isRunning_ = False

    def taskFuncPointer( self ) : return self.__taskFuncPointer_

    def isRunning( self ) :
        return self.__isRunning_ and self.__workerThread_.isAlive()

    def start( self ):
        if not self.__isRunning_ :
            self.__isRunning_ = True
            self.__workerThread_ = self.WorkerThread( self )
            self.__workerThread_.start()

    def stop( self ) : self.__isRunning_ = False

    class WorkerThread( threading.Thread ):
        def __init__( self, bgTask ):
            threading.Thread.__init__( self )
            self.__bgTask_ = bgTask

        def run( self ):
            try :
                self.__bgTask_.taskFuncPointer()( self.__bgTask_.isRunning )
            except Exception as e: print repr(e)
            self.__bgTask_.stop()

def tkThreadedGUI():
    class App(tk.Frame):

        def __init__(self):
            super(App, self).__init__()

        def __init__(self, master):
            tk.Frame.__init__(self, master)

            self.dict = self.dictread('./Samples/')
            
            self.top = Frame(self.master)
            self.bottom = Frame(self.master)
            self.top.pack(side=TOP)
            self.bottom.pack(side=BOTTOM, expand=True)

            self.sampleset = tk.StringVar(self)
            self.sample_l = tk.StringVar(self)
            self.sample_r = tk.StringVar(self)

            self.sampleset.trace('w', self.update_folder)
            self.sample_l.trace('w', self.update_samples)
            self.sample_r.trace('w', self.update_samples)

            self.dropdwn_folder = tk.OptionMenu(self, self.sampleset, *list(self.dict.keys()))
            self.dropdwn_l = tk.OptionMenu(self, self.sample_l, '')
            self.dropdwn_r = tk.OptionMenu(self, self.sample_r, '')

            self.sampleset.set(self.dict.keys()[0])

            self.snd_l = self.sample_l.get()
            self.snd_r = self.sample_r.get()

            self.dropdwn_folder.pack()
            self.dropdwn_l.pack(pady = 10)
            self.dropdwn_r.pack(pady = 10)
            self.pack(pady = 20)
            
            
            self.speedlabel = tk.Label(self.master, text="Speed:")
            self.speedlabel.pack()
            self.speed = tk.Scale(self.master, from_=0, to=5, 
				resolution = 0.1, orient=HORIZONTAL, bg="white")
            self.speed.set(1)
            self.speed.pack(fill=X, pady = 1)
            self.playspeed = float(self.speed.get())


            self.startButton = tk.Button(
            self.master, text="START SERVER", command=self.onStartClicked )
            self.startButton.pack(in_=self.bottom, side=LEFT)

            self.cancelButton = tk.Button(
            self.master, text="Stop Server", command=self.onStopClicked, fg="red" )
            self.cancelButton.pack(in_=self.bottom, side=LEFT)


            self.bgTask = BackgroundTask( self.audioProcess )

        def onStartClicked( self ):
            print "onStartClicked"
            try: 
				self.bgTask.start()
            except: pass

        def onStopClicked( self ) :
            print "onStopClicked"
            try: 
				self.bgTask.stop()
            except: pass


        def update_folder(self, *args):
            samples = self.dict[self.sampleset.get()]
            self.sample_l.set(samples[0])
            self.sample_r.set(samples[0])

            menu_l = self.dropdwn_l['menu']
            menu_l.delete(0, 'end')

            menu_r = self.dropdwn_r['menu']
            menu_r.delete(0, 'end')

            for sample in samples:
                menu_l.add_command(label=sample, command=lambda samplefile=sample: self.sample_l.set(samplefile))
                menu_r.add_command(label=sample, command=lambda samplefile=sample: self.sample_r.set(samplefile))

        def update_samples(self, *args):
            self.getsample_l = self.sample_l.get()
            self.getsample_r = self.sample_r.get()

        def dictread(self, folder):
            self.file_dict = {}
            sampledirs = glob(folder + '*/')
            for sampledir in sampledirs:
                print(sampledir)
                self.file_dict[sampledir] = glob(sampledir + '*.wav')
            return(self.file_dict)

        def audioProcess( self, isRunningFunc=None ) :
			s = Server(sr=44100, nchnls=4, buffersize=512, duplex=1)
			s.setInOutDevice(2)
			s.boot()
			sl = SfPlayer(self.snd_l)
			sdl = SmoothDelay(sl, delay=0.0, feedback=0.5, crossfade=0.05, mul=0.5).out(chnl=1)
			sr = SfPlayer(self.snd_r)
			sdr = SmoothDelay(sr, delay=0.0, feedback=0.5, crossfade=0.05, mul=0.5).out(chnl=2)
			s.start()
			while True:
				try:
					if not isRunningFunc():
						print("Server Stopped!")
						return
				except : pass
				self.playspeed = float(self.speed.get())
				l_sample = self.sample_l.get()
				r_sample = self.sample_r.get()
				sr.setPath(l_sample)
				sl.setPath(r_sample)
				sr.play()
				sleep(self.playspeed)
				sl.play()
				sleep(self.playspeed)
				

    root = tk.Tk()
    root.title("TECHNO BITCH!")
    root.geometry("600x600")
    app = App(root)
    app.mainloop()


if __name__ == "__main__":
    tkThreadedGUI()
