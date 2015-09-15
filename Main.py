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
        try:
            while running:
                self._mainloop.update()
                self._mainloop.draw()
        finally:
            self._mainloop.cleanUp()


if __name__ == "__main__":
    gl=Main()
    gl.run()

