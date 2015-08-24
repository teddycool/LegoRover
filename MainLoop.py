__author__ = 'teddycool'
#State-switching and handling of general rendering

from Cam import Cam
import time
from Sensors import Sensors
from Driver import MotorControl

import RPi.GPIO as GPIO

class MainLoop(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        #self._sensors= Sensors.Sensors(GPIO)
        self._driver = MotorControl.MotorControl(GPIO)




    def initialize(self):
        print "Main init..."
        self._cam.initialize()
        self.time=time.time()
        #Init all states
        for key in self._state.keys():
            self._state[key].initialize()
        print "Game started at ", self.time

    def update(self,screen):
        self._cam.update()
        pos = 0
        return pos

    def draw(self, screen):
        #Move partly to StateLoops
        self._inputs.draw(screen)

        cam = self._currentStateLoop.draw(self._cam.csnapshot)
        screen.blit(cam, (0,0))
        return screen

    def changeState(self, newstate):
        if (newstate == 0) or (newstate == "InitState"):
            self._currentStateLoop = CamCalibrateLoop.CamCalibrateLoop()

        self._currentStateLoop.initialize()
        return newstate

    def cleanUp(self):
        #cleanup all packages...
        GPIO.cleanup()


