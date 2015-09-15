__author__ = 'teddycool'
#State-switching and handling of general rendering

from Vision import Cam
import time
from Sensors import Sensors
from Driver import MotorControl
from Vision import Vision

import RPi.GPIO as GPIO

class MainLoop(object):
    def __init__(self):
        self._state ={}
        GPIO.setmode(GPIO.BCM)
        self._driver = MotorControl.MotorControl(GPIO)
        self._sensors = Sensors()




    def initialize(self):
        print "MainLoop init..."
        self.time=time.time()
        #Init all states
        for key in self._state.keys():
            self._state[key].initialize()
        print "Game started at ", self.time


# 1 grab image from picamera stream
# 2 handle image analyze
# 3 read sensordata (maybe not every frame?
# 3 use analyze output to control rover
# 4 publish image with control overlay to video-streamer


    def update(self,screen):

        pos = 0
        return pos

    def draw(self, screen):
        return

    def changeState(self, newstate):
        if (newstate == 0) or (newstate == "InitState"):
            self._currentStateLoop = CamCalibrateLoop.CamCalibrateLoop()

        self._currentStateLoop.initialize()
        return newstate

    def cleanUp(self):
        #cleanup all packages...
        GPIO.cleanup()


