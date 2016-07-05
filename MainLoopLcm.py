__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import Sensors
from Vision import Vision
import lcm
from LCM import usdistance

import thread

#Global GPIO used by all...
import RPi.GPIO as GPIO
import os

class MainLoop(object):
    def __init__(self):
        self._state ={}
        self._gpio = GPIO
        self._gpio.setmode(self._gpio.BCM)

        self._sensors = Sensors.Sensors(self._gpio)
        self._vision = Vision.Vision((1024,768))
       #self._compass =

    def initialize(self):
        print "MainLoop LCM init..."
        print "Starting timers..."
        self.time=time.time()
        print "Kickstart runner for RangeSensors in separate process"
        os.system('sudo python UsMain.py &')
        frame = self._vision.initialize()
        self._sensors.initialize()
        #print "Starting new thread for electronic compass"
        print "MainLoop initialized"
        #TODO: Initialize vision in separate process and take care of vision-data (rectangles) by using LCM
        return frame


    def draw(self,frame):
        #Handle values...
        self._sensors.draw(frame)
        frame = self._sensors.draw(frame)
        self._vision.draw(frame)
        return

    def update(self):
        self._sensors.update()
        frame = self._vision.update()
        return frame

    def __del__(self):
        self._gpio.cleanup()
        print "MainLoop cleaned up"


