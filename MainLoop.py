__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import Sensors
from Driver import Driver
from Vision import Vision


#Global GPIO used by all...
import RPi.GPIO as GPIO
import os

class MainLoop(object):
    def __init__(self):
        self._state ={}
        GPIO.setmode(GPIO.BCM)
        self._gpio = GPIO
        self._driver = Driver.Driver(self._gpio)
        self._sensors = Sensors.Sensors(self._gpio)
        self._vision = Vision.Vision((640,480))


    def initialize(self):
        print "MainLoop init..."
        print "Starting timers..."
        self.time=time.time()
        self._vision.initialize()
        self._sensors.initialize()
        self._driver.initialize()
        print "Rover started at ", self.time

    def update(self):
        #TODO: add update-freq from config
        self._sensors.update()
        #TODO: add vision update...
        self._vision.update()
       # self._driver.update(self._sensors.sensorvaluesdict)
        time.sleep(0.01)

    def draw(self):
        #TODO: add update-freq from config
        frame = self._vision.getCurrentFrame()
        frame = self._sensors.draw(frame)
        frame = self._driver.draw(frame)
        frame = self._vision.draw(frame)

    def __del__(self):
        GPIO.cleanup()
        print "MainLoop cleaned up"