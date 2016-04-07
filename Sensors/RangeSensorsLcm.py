#This handles a set/list of rangesensors
#These sensors could not be activated at the same time but only one at a time to not interfere with each other
# rangsensordefinitions = [['channelname', triggerpin, echopin], ['channelname', triggerpin, echopin]....


import time
import cv2
import lcm
from LCM import usdistance

class RangeSensor(object):

    def __init__(self, gpio, rangesensordefinition):
        self._gpio = gpio
        self._gpio.setmode(self._gpio.BCM)
        self._channelName = rangesensordefinition[0]
        self._TRIG = rangesensordefinition[1]
        self._ECHO = rangesensordefinition[2]
        self._lastrange = 0
        self._history = []

        self._gpio.setup(self._TRIG,self._gpio.OUT)
        self._gpio.setup(self._ECHO,self._gpio.IN)

        self._gpio.output(self._TRIG, False)

        self._msg = usdistance.usdistance()
        self._msg.name = self._channelName
        self._msg.enabled = True

        print "Started range-sensor on pin: " + str(self._ECHO) + " for msg channel " + self._channelName

    def update(self):
        self._gpio.output(self._TRIG, True)
        time.sleep(0.01)  # Triggertime-high
        self._gpio.output(self._TRIG, False)
        pulse_start = time.time()
        echo_start = time.time()
        echo_end = time.time()
        # TODO: fix a timeout...
        while self._gpio.input(self._ECHO) == 0:
            echo_start = time.time()
            if time.time() - pulse_start > 0.1:
                break

        while self._gpio.input(self._ECHO) == 1:
            echo_end = time.time()
            if time.time() - pulse_start > 0.2:
                break

        pulse_duration_max = echo_end - pulse_start
        pulse_duration_min = echo_start - pulse_start
        pulse_duration = echo_end - echo_start
        # distance = high level time * sound-velocity (340M/S) / 2
        # dataspec suggest to use over 60ms measurement cycle, in order to prevent trigger signal to the echo signal.
        distance_max = pulse_duration_max * 17000
        distance_max = round(distance_max, 2)
        distance_min = pulse_duration_min * 17000
        distance_min = round(distance_min, 2)
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        self._lastrange = distance
        self._msg.distance = self._lastrange

        #TODO: Fix history


class RangeSensorsLcm(object):
    
    def __init__(self, gpio, rangesensorlist):
        self._rangeSensors = []
        self._lc = lcm.LCM()

        for rangesensor in rangesensorlist:
            self._rangeSensors.append(RangeSensor(gpio,rangesensor))
        
        print "Stabilizing rangesensors...."
        time.sleep(2)

       
    def update(self, kwarg):
        while 1:
            #print "Update in the new thread..."
            for range in self._rangeSensors:
                range.update()
                self._lc.publish(range._channelName, range._msg.encode())
                #print "Distance RangeSensor pin " + str(range._ECHO) + ": " + range._channelName
                time.sleep(0.05)



        
if __name__ == '__main__':
    print "Testcode for range sensor"
    import lcm
    import RPi.GPIO as GPIO
    import thread
    GPIO.setmode(GPIO.BCM)
    #Fix to use import from correct package...
    def my_handler(channel, data):
        msg = usdistance.usdistance.decode(data)
        print("Received message on channel \"%s\"" % channel)
        print("   name        = '%s'" % msg.name)
        print("   distance    = %s" % str(msg.distance))
        print("   enabled     = %s" % str(msg.enabled))

    lc = lcm.LCM()
    rangsensors = RangeSensorsLcm(GPIO, [["RS1", 23,24],["RS2", 20,21]])
    subscription1 = lc.subscribe("RS1", my_handler)
    subscription1 = lc.subscribe("RS2", my_handler)
    thread.start_new_thread(rangsensors.update,(None,) )
    try:
        while 1:
            lc.handle()
            time.sleep(0.1)

    except Exception as e:
        print str(e)
        GPIO.cleanup()
