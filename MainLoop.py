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
        self._vision = Vision.Vision((640,480))
        self._vu_time = 0;

    def initialize(self):
        print "MainLoop init..."
        print "Starting timers..."
        self.time=time.time()
        self._vision.initialize()
        self._driver.initialize()
        print "Rover started at ", self.time

    def update(self):
        t_start = time.time()
        self._vision.update()
        self._vu_time = (time.time()-t_start)*0.25 + self._vu_time*0.75
        print "Vision update: " + str(self._vu_time)
        target = self._vision.getCurrentTargetX()
        targetFound = self._vision.getTargetFound()
        self._driver.update(target, targetFound)

    def draw(self):
        #TODO: add update-freq from config
        frame = self._vision.getCurrentFrame()
        target = self._vision.getCurrentTargetX()
        targetFound = self._vision.getTargetFound()
        frame = self._driver.draw(frame, target, targetFound)
        frame = self._vision.draw(frame)

    def __del__(self):
        GPIO.cleanup()
        print "MainLoop cleaned up"