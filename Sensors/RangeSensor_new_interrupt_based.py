
import time
import cv2
#import RPi.GPIO as GPIO

class RangeSensor(object):
    
    def __init__(self, gpio, triggerpin, echopin, sample_time = 0.2):
        self._gpio = gpio
        #self._gpio.setmode(self._gpio.BCM)
        self.TRIG = triggerpin
        self.ECHO = echopin
        self.distance = 0
        self.ValueUpdated = False
        self.startTime = 0
        self.trigCount = 0
        self._sample_time = sample_time

        print "Distance Measurement initialized for pin: " + str(echopin)
        
        self._gpio.setup(self.TRIG,self._gpio.OUT)
        self._gpio.setup(self.ECHO,self._gpio.IN)
        
        self._gpio.output(self.TRIG, False)
        print "Stabilizing range-sensor on pin: " + str(echopin)
        time.sleep(1)
        self._gpio.add_event_detect(self.ECHO, self._gpio.BOTH, callback = self.EdgeEchoPin)
        self.trig()

    def EdgeEchoPin(self, channel):
        if channel == self.ECHO:
            print "Callback from:" + str(channel)
            if self._gpio.input(channel) == 1:
                self.startTime = time.time()
            else:
                self.distance = (time.time() - self.startTime) * 17000
                self.ValueUpdated = True
                self.trig()


    def trig(self):
        time.sleep(self._sample_time)
        self.trigCount += 1
        self.ValueUpdated = False
        self._gpio.output(self.TRIG, True)
        time.sleep(0.01) #Triggertime-high
        self._gpio.output(self.TRIG, False)

    def update(self):
        print "Distance RangeSensor pin " + str(self.ECHO) + ": " + str(self.distance) + " TrigCount=" + str(self.trigCount)
        return self.distance

    def draw(self, frame, name, textstartx, textstarty):
        cv2.putText(frame, name + ": " + str(self.distance) + " cm", (textstartx,textstarty),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame

if __name__ == '__main__':
    print "Testcode for interrupt-based range sensor"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    rs1 = RangeSensor(GPIO, 23, 24)
    rs2 = RangeSensor(GPIO, 20, 21)
    try:
        while 1:
            print "RS2: " + str(rs2.update())
            print "RS1: " + str(rs1.update())

            time.sleep(0.1)
    except Exception as e:
        print str(e)
        GPIO.cleanup()
