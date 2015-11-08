__author__ = 'teddycool'

#logic for driving...
#using MotorControl and sensor values

import MotorControl

class Driver(object):


    def __init__(self, GPIO):
        self._gpio = GPIO
        self._mc = MotorControl.MotorControl(self._gpio)
        self._drivemodes = ["FwdFast", "FwdSlow", "Stop", "RevFast", "RevSlow", "TRight", "TLeft"]
        return


    def initialize(self):
        self._mc.stop()
        return

    def update(self, sensorvaluesdict):
        if sensorvaluesdict["UsFrontLeftDistance"]["Current"] > 30:
            self._mc.forward()
            self._mc.setSpeed(50)

        if sensorvaluesdict["UsFrontLeftDistance"]["Current"] < 10:
            self._mc.reverse()
            self._mc.setSpeed(50)
        return

    def draw(self, frame):
        return frame

    def __del__(self):
        print "Driver object deleted..."
        self._mc.stop()
