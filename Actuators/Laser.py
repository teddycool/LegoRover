__author__ = 'teddycool'

class Laser(object):
    def __init__(self, GPIO, controlpin=21):
        self._gpio = GPIO
        self._pin = controlpin
        self._gpio.setup(self._pin,self._gpio.OUT, initial=0)

    def activate(self, on):
        self._gpio.output(self._pin, on)

    def __del__(self):
        print "Laser object deleted..."
        self.activate(False)


if __name__ == '__main__':
    print "Testcode for Laser"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    import time
    las1 = Laser(GPIO, 20)
    las2 = Laser(GPIO, 21)
    while True:
        las1.activate(True)
        las2.activate(True)
        time.sleep(1)
        las1.activate(False)
        las2.activate(False)
    GPIO.cleanup()