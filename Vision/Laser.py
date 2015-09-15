__author__ = 'teddycool'

class Laser(object):
    def __init__(self, GPIO, controlpin):
        self._gpio = GPIO
        self._pin = controlpin
        self._gpio.setup(self._pin,self._gpio.OUT, initial=0)

    def activate(self, on):
        self._gpio.output(self._pin, on)



if __name__ == '__main__':
    print "Testcode for Laser"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    import time
    laser = Laser(GPIO, 21)
    laser.activate(True)
    time.sleep(2)
    laser.activate(False)
    GPIO.cleanup()


