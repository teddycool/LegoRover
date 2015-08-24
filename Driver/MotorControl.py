__author__ = 'psk'
#Handles the actual motors


class MotorControl(object):

    def __init__(self, GPIO):
        self._gpio = GPIO
        #Bool except Speed which is pwm
        self._controlGPIOs={'LeftOn': 5,'LeftRev': 6, 'RightOn':13,  'RightRev': 19, 'Speed':26}
        self._controlStates = {'LeftOn': False,'LeftRev': False, 'RightOn':False,  'RightRev': False, 'Speed':0}
        for gpio in self._controlGPIOs:
            self._gpio.setup(self._controlGPIOs[gpio],self._gpio.OUT, initial=0)

    def start(self):
        self._controlStates['LeftOn']=True
        self._controlStates['RightOn'] = True

    def stop(self):
        self._controlStates['LeftOn']=False
        self._controlStates['RightOn'] = False

    def update(self):
        self._setMotorStates()


    def _setMotorStates(self):
        for state in self._controlStates:
            #Set gpios according to current states...
            print state, self._controlGPIOs[state],  self._controlStates[state]
            self._gpio.output(self._controlGPIOs[state], self._controlStates[state])


if __name__ == '__main__':
    print "Testcode for Driver"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    import time
    mc= MotorControl(GPIO)
    mc.start()
    mc.update()
    time.sleep(2)
    mc.stop()
    mc.update()
    GPIO.cleanup()
