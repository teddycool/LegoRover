__author__ = 'teddycool'

# logic for driving...
# using MotorControlL298 and sensor values

import cv2
from MotorControl import MotorControlLegoIr8884


# from MotorControl import MotorControlL298



class Driver(object):
    def __init__(self, GPIO):
        self._gpio = GPIO
        # self._gpio.setmode(self._gpio.BCM)
        # self._mc = MotorControlL298.MotorControlL298(self._gpio)
        self._mc = MotorControlLegoIr8884.MotorControlLegoIr8884(self._gpio)
        self._drivemodes = ["FwdFast", "FwdSlow", "Stop", "RevFast", "RevSlow", "TRight", "TLeft"]
        self._driverStates = {}
        # driverStateList = [" " ]
        return

    def initialize(self):
        self._mc.setMotion(0, 0)
        return

    def update(self, sensorvaluesdict):
        # TODO: Fix driver-states
        print "Driver update"
        # if sensorvaluesdict["UsFrontLeftDistance"]["Current"] > 50 and sensorvaluesdict["UsFrontRightDistance"]["Current"] > 50:
        #     self._mc.forward()
        #     self._mc.setSpeed(100)
        #
        # if sensorvaluesdict["UsFrontLeftDistance"]["Current"] < 30 and sensorvaluesdict["UsFrontRightDistance"]["Current"] > 50:
        #     self._mc.rightTurn()
        #     self._mc.setSpeed(50)
        #
        # if sensorvaluesdict["UsFrontLeftDistance"]["Current"] > 50 and sensorvaluesdict["UsFrontRightDistance"]["Current"] < 30:
        #     self._mc.leftTurn()
        #     self._mc.setSpeed(50)
        #
        # if sensorvaluesdict["UsFrontLeftDistance"]["Current"] < 10 or sensorvaluesdict["UsFrontRightDistance"]["Current"] < 10:
        #     self._mc.reverse()
        #     self._mc.setSpeed(50)

        self._mc.setMotion(0, 0)
        return

    def draw(self, frame):
        # cv2.putText(frame,"Speed: " + str(self._mc._currentSpeed) ,(5,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.putText(frame, "Motor: " + str(self._mc._controlStates), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2)

        return frame

    def __del__(self):
        self._mc.setMotion(0, 0)
        print "Driver object deleted..."
