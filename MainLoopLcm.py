__author__ = 'teddycool'
#State-switching and handling of general rendering

import time

from Sensors import RangeSensorLcm
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
        self._us1=RangeSensorLcm.RangeSensorLcm(self._gpio ,23,24) #Trig, echo
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

    def update(self):
        self._us1.update()
        time.sleep(0.01)

    def draw(self):
        self._lc.handle()
        pass

    def __del__(self):
        GPIO.cleanup()
        print "MainLoop cleaned up"