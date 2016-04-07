__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import RangeSensorsLcm
import lcm
from LCM import usdistance


#Global GPIO used by all...
import RPi.GPIO as GPIO
import os

class MainLoop(object):
    def __init__(self):
        self._state ={}
        GPIO.setmode(GPIO.BCM)
        self._gpio = GPIO
        self._us=RangeSensorsLcm.RangeSensorsLcm(self._gpio, [["RS1", 23,24],["RS2", 20,21]])
        self._lc = lcm.LCM()
        self._subscription = self._lc.subscribe("ULTRASONIC", self.my_handler)

    def my_handler(self, channel, data):
        msg = usdistance.decode(data)
        print("Received message on channel \"%s\"" % channel)
        print("   name        = '%s'" % msg.name)
        print("   distance    = %s" % str(msg.distance))
        print("   enabled     = %s" % str(msg.enabled))


    def initialize(self):
        print "MainLoop LCM init..."
        print "Starting timers..."
        self.time=time.time()

    def update(self, us): #In new thread
        while 1:
            print "Update in the new thread..."
            us.update()
            time.sleep(0.01)

    def draw(self):
        self._lc.handle()
        pass

    def __del__(self):
        GPIO.cleanup()
        print "MainLoop cleaned up"