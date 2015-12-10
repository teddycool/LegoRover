__author__ = 'teddycool'

import os, sys
from MainLoop import MainLoop
from Logger import Logger

class Main(object):

    def __init__(self):
        print "Init Main object..."
        self._mainloop =  MainLoop()
        self._log = Logger.Logger('main')


    def run(self):

        self._mainloop.initialize()
        running=True
        frames = 0
        while running:
            try:
                frames = frames + 1
                self._log.info("Entering main-loop....")
                self._mainloop.update()
                #Not all  has to be drawn
                if frames%3==0:
                    self._mainloop.draw()
            except Exception as e:
                 print str(e)


if __name__ == "__main__":
    print 'Started from: Main.py,  if __name__ == "__main__" '
    gl=Main()
    gl.run()

