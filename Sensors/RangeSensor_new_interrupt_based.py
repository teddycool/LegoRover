
import time
from threading import Thread
#import cv2
#import RPi.GPIO as GPIO


class RangeSensor(object):
    
    def __init__(self, gpio, triggerpin, echopin, sample_time = 0.2):
        self._gpio = gpio
        #self._gpio.setmode(self._gpio.BCM)
        self.TRIG = triggerpin
        self.ECHO = echopin
        self.distance = 0
        self.trigged = False
        self.startTime = 0
        self.trigCount = 0
        self._sample_time = sample_time
        self.values = [0] * 10
        self._sampling = False


        print "Distance Measurement initialized for pin: " + str(echopin)
        
        self._gpio.setup(self.TRIG,self._gpio.OUT,initial = self._gpio.LOW)
        self._gpio.setup(self.ECHO,self._gpio.IN)

        print "Stabilizing range-sensor on pin: " + str(echopin)
        time.sleep(2)
        try:
            self._gpio.add_event_detect(self.ECHO, self._gpio.BOTH, callback = self.EdgeEchoPin)
        except:
            print 'Can not set edge detection on pin: ' + str(self.ECHO) + ', try again!'
            self._gpio.remove_event_detect(self.ECHO)
            self._gpio.add_event_detect(self.ECHO, self._gpio.BOTH, callback = self.EdgeEchoPin)

        self.trig()

    def cleanup(self):
        self.stop_sampling()
        self._gpio.remove_event_detect(self.ECHO)
        time.sleep(self._sample_time)

    def set_sample_time(self, sample_time):
        self._sample_time = sample_time


    def EdgeEchoPin(self, channel):
        if channel == self.ECHO:
            if self._gpio.input(channel) == 1:
                self.startTime = time.time()
            else:
                self.distance = (time.time() - self.startTime) * 17000
                self.values.pop()
                self.values.insert(0, [self.distance])


    def trig(self):
        self._gpio.output(self.TRIG, True)
        time.sleep(0.01) #Triggertime-high
        self._gpio.output(self.TRIG, False)
        self.trigged = True

    def start_sampling(self):
        self._sampling = True
        sample_t = Thread(target=self.main_sampler).start()


    def main_sampler(self):
        while self._sampling:
             time.sleep(self._sample_time)
             self.trig()

    def stop_sampling(self):
        self._sampling = False

    def update(self):
        print "Distance RangeSensor pin " + str(self.ECHO) + ": " + str(self.get_values()[0])
        return self.distance

    def draw(self, frame, name, textstartx, textstarty):
        cv2.putText(frame, name + ": " + str(self.distance) + " cm", (textstartx,textstarty),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame

    def get_values(self):
        return self.values

if __name__ == '__main__':
    print "Testcode for interrupt-based range sensor"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    rs1 = RangeSensor(GPIO, 23, 24)
    rs2 = RangeSensor(GPIO, 21, 22)
    rs1.start_sampling()
    while 1:
        time.sleep(0.4)
        rs1.update()
    time.sleep(2)
    print rs1.distance

    '''
    try:
        for x in range(1,10):
            print "RS2: " + str(rs2.update())
            print "RS1: " + str(rs1.update())
            rs1.trig()
            rs2.trig()
            time.sleep(0.5)
    except Exception as e:
        print str(e)
    except KeyboardInterrupt:
        print 'key int Exit'
    except:
        print 'oth excep'
    finally:
        rs1.cleanup()
        rs2.cleanup()
        GPIO.cleanup()
    '''
    rs1.cleanup()
    rs2.cleanup()
    GPIO.cleanup()

