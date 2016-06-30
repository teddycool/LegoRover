__author__ = 'teddycool'
#Manage all sensors
import RangeSensorsLcm
import copy
import time
import lcm
from LCM import usdistance
import thread
import cv2

from Logger import Logger


class Sensors(object):
    def __init__(self, gpio):
        self._gpio = gpio
        self.sensorvaluesdict={}
        valuesdict = {"Current": 0, "TrendList": []}
        channels = ["RS1", "RS2", ] # ,"BarometricPressure", "Temperature", "Light", "Accelerometer", "Gyro","IrFrontDistance" ]
        for channel in channels:
            self.sensorvaluesdict[channel]= copy.deepcopy(valuesdict)
        print "Created values dictionary..."
        self._lc = lcm.LCM()
        #Add subscriptions for all messages
        self._s1 = self._lc.subscribe("RS1", self._usd_handler)
        self._s2 = self._lc.subscribe("RS2", self._usd_handler)
        self._log = Logger.Logger("sensors")

    def __del__(self):
        self._lc.unsubscribe(self._s1)
        self._lc.unsubscribe(self._s2)

    def initialize(self):
         self._log.info("Sensors init")


    def update(self):
        self._log.info("Sensors update started")
        self._lc.handle()


    def draw(self, frame):
        self._log.info("Sensors draw started")
        index = 10
        for channel in self.sensorvaluesdict:
            cv2.putText(frame, channel + ": " + str(self.sensorvaluesdict[channel]["Current"]), (index,50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            index = index + 100
        return frame



    def _updateValuesList(self,value, valuelist):
        if value != "N/A":
            valuelist.append(float(value))
            if (len(valuelist)> 10):
                poped = valuelist.pop(0)
        return valuelist


#private callback functions
    def _usd_handler(self, channel, data):
        print("Received message on channel \"%s\"" % channel)
        msg = usdistance.usdistance.decode(data)
        self.sensorvaluesdict[channel]["Current"] = msg.distance
        self._updateValuesList(msg.distance, self.sensorvaluesdict[channel]["TrendList"])
        print str(self.sensorvaluesdict[channel])


