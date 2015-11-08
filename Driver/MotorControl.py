__author__ = 'teddycool'
#Handles the actual motors


class MotorControl(object):

    def __init__(self, GPIO):
        self._gpio = GPIO
        #Bool except Speed which is pwm
        #TODO: fix statet to left/rigth -> fwd, rev, off
        self._controlGPIOs={'LeftOn': 5,'LeftRev': 6, 'RightOn':13,  'RightRev': 19}
        self._controlStates = {'LeftOn': False,'LeftRev': False, 'RightOn':False,  'RightRev': False}
        for gpio in self._controlGPIOs:
            self._gpio.setup(self._controlGPIOs[gpio],self._gpio.OUT, initial=0)

        self._speedGpio = self._gpio.setup(26,self._gpio.OUT )
        self._speedGpio =  self._gpio.PWM(26, 200) #Pin 26 for speed control and using 200 hz
        self._currrentSpeed = 100
        self._speedGpio.start(self._currrentSpeed)  #Start att full speed...


    def reverse(self):
        self._controlStates['LeftOn']=True
        self._controlStates['RightOn'] = True
        self._controlStates['LeftRev']=False
        self._controlStates['RightRev'] = False
        self._setMotorStates()

    def forward(self):
        self._controlStates['LeftOn']=False
        self._controlStates['RightOn'] = False
        self._controlStates['LeftRev']=True
        self._controlStates['RightRev'] = True
        self._setMotorStates()

    def stop(self):
        self._controlStates['LeftOn']=False
        self._controlStates['RightOn'] = False
        self._controlStates['LeftRev']=False
        self._controlStates['RightRev'] = False
        self._setMotorStates()

    def rightTurn(self):
        self._controlStates['LeftOn']=True
        self._controlStates['RightRev'] = True
        self._setMotorStates()

    def leftTurn(self):
        self._controlStates['LeftRev']= True
        self._controlStates['RightOn'] = True
        self._setMotorStates()

    def setSpeed(self, speed):
        self._currrentSpeed = speed
        self._speedGpio.ChangeDutyCycle(speed)

    def getCurrent(self):
        return self._controlStates, self._currrentSpeed



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
    mc.setSpeed(100)
    print mc.getCurrent()
    mc.forward()
    time.sleep(4)
    mc.setSpeed(20)
    print mc.getCurrent()
    time.sleep(4)
    mc.stop()
    print mc.getCurrent()
    time.sleep(2)
    mc.rightTurn()
    print mc.getCurrent()
    time.sleep(2)
    mc.reverse()
    print mc.getCurrent()
    #mc.setSpeed(10)
    time.sleep(4)
    mc.stop()
    print mc.getCurrent()
    GPIO.cleanup()
