__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import Sensors
from Driver import Driver
from Vision import Vision
from Actuators import Laser


#Global GPIO used by all...
import RPi.GPIO as GPIO

class MainLoop(object):
    def __init__(self):
        self._state ={}
        GPIO.setmode(GPIO.BCM)
        self._gpio = GPIO
        self._driver = Driver.Driver(self._gpio)
        self._sensors = Sensors.Sensors(self._gpio)
        self._vision = Vision.Vision((640,480))
        self._laser = Laser.Laser(self._gpio,25)


    def initialize(self):
        print "MainLoop init..."
        self.time=time.time()
        self._vision.initialize()
        self._sensors.initialize()
        self._laser.activate(True)
        self._driver.initialize()
        print "Rover started at ", self.time

    def update(self):
        self._frame = self._vision.update()
        self._sensors.update()
        self._driver.update(self._sensors.sensorvaluesdict)
        time.sleep(0.01)

    def draw(self):
        self._frame  = self. _sensors.draw(self._frame)
        self._vision.draw(self._frame)

    def cleanUp(self):
        #cleanup all packages...
        self._laser.activate(False)
        self._driver.stop()
        GPIO.cleanup()
        print "MainLoop cleaned up"


