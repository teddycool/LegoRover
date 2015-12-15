__author__ = 'teddycool'
#Manage all sensors
import RangeSensor
import copy
import time
import config
import Compass
#import AccelGyro
import cv2
from Logger import Logger


class Sensors(object):
    def __init__(self, GPIO):
        self._gpio = GPIO
        self.sensorvaluesdict={}
        valuesdict = {"Current": 0, "TrendList": []}
        sensors = ["UsFrontLeftDistance", "Compass", "UsFrontRightDistance"] # ,"BarometricPressure", "Temperature", "Light", "Accelerometer", "Gyro","IrFrontDistance" ]
        for sensor in sensors:
            self.sensorvaluesdict[sensor]= copy.deepcopy(valuesdict)
        print "Created values dictionary..."
        self._rangeRight = RangeSensor.RangeSensor(self._gpio,23,24)
        self._rangeLeft = RangeSensor.RangeSensor(self._gpio,20,21) #Trig, echo
        self._compass= Compass.Compass()
        self._log = Logger.Logger("sensors")

    def initialize(self):
        #connect each variable to the sensor and value
        self._log.info("Sensors init")
        self._compass.initialize()
        self._updateValues()


    def update(self):
        self._log.info("Sensors update started")
        self._updateValues()

    def draw(self, frame):
        self._log.info("Sensors draw started")
        frame = self._rangeLeft.draw(frame, "USL", 20,460)
        frame = self._rangeRight.draw(frame,"USR", 460, 460)
        frame = self._compass.draw(frame, 220,460)
        return frame

    def _updateValues(self):
        #TODO: fix automatic update-call for each sensor -> .update()
        print "Updating sensor values started"
        startime= time.time()

        self.sensorvaluesdict["UsFrontRightDistance"]["Current"] = self._rangeRight.update()
      #  print "Updating sensor values: UsFrontRigthDistance"

        self.sensorvaluesdict["UsFrontLeftDistance"]["Current"] = self._rangeLeft.update()
       # print "Updating sensor values: UsFrontLeftDistance"

        self.sensorvaluesdict["Compass"]["Current"] = self._compass.update()
        #print "Updating sensor values: Compass"

        for key in self.sensorvaluesdict:
            self.sensorvaluesdict[key]["TrendList"] = self._updateValuesList(self.sensorvaluesdict[key]["Current"], self.sensorvaluesdict[key]["TrendList"] )
        #print "Updating sensor values finished: " + str(time.time())
        print "Updatetime sensors: " + str(time.time()-startime)


    def _updateValuesList(self,value, valuelist):
        if value != "N/A":
            valuelist.append(float(value))
            if (len(valuelist)> 10):
                poped = valuelist.pop(0)
        return valuelist

