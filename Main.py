__author__ = 'teddycool'

import os, sys
from MainLoop import MainLoop


class Main(object):

    def __init__(self):
        print "Init Main object..."
        self._mainloop =  MainLoop()


    def run(self):
        self._mainloop.initialize()
        running=True
        while running:
            try:
                self._mainloop.update()
                self._mainloop.draw()
            except Exception as e:
                 print str(e)
                 running = False

        self._mainloop.cleanUp()
        print "Game over..."


if __name__ == "__main__":
    print 'Started from: Main.py,  if __name__ == "__main__" '
    gl=Main()
    gl.run()

