__author__ = 'psk'
#Manage all sensors
import RangeSensor

class Sensors(object):
    def __init__(self):
        import copy
        self.sensorvaluesdict={}
        valuesdict = {"Current": 0, "TrendList": []}
        measurements = ["IndoorTemp","OutdoorTemp", "IndoorHum", "OutdoorHum", "OutdoorBar","FridgeTempUpper", "FridgeTempLower", "FreezerTemp"]
        for meassure in measurements:
            self.sensorvaluesdict[meassure]= copy.deepcopy(valuesdict)

        self._rangeFwd=RangeSensor()

        return

    def initialize(self):
        #connect each variable to the sensor and value
        #self._updateValues()
        return

    def update(self):
         self._updateValues()
         return


    def update(self):
         self._updateValues()
         return

    def _updateValues(self):
        print "Updating sensor values"
        #Read values from sensor with more then one returnvalue
        indoor= self._indoor.read()
        outdoor = self._outdoor.read()
        self.sensorvaluesdict["FridgeTempUpper"]["Current"] = self._fridgeSensorUpper.read_temp()[0]
        self.sensorvaluesdict["OutdoorBar"]["Current"] = self._outdoorBar.readPressure()
        self.sensorvaluesdict["IndoorHum"]["Current"] = indoor[0]
        self.sensorvaluesdict["IndoorTemp"]["Current"] = indoor[1]
        self.sensorvaluesdict["OutdoorHum"]["Current"] = outdoor[0]
        self.sensorvaluesdict["OutdoorTemp"]["Current"] = outdoor[1]
