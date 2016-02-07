__author__ = 'teddycool'
#Handles the actual motors  wow wow wow
from IMotionControl import IMotionControl


class MotorControlL298(IMotionControl):

    def __init__(self, GPIO):
        super(MotorControlL298, self).__init__()
        self._gpio = GPIO
        #Bool except Speed which is pwm
        #TODO: fix statet to left/rigth -> fwd, rev, off
        self._controlGPIOs={'LeftOn': 5,'LeftRev': 6, 'RightOn':13,  'RightRev': 19}
        self._controlStates = {'LeftOn': True,'LeftRev': False, 'RightOn':True,  'RightRev': False}
        for gpio in self._controlGPIOs:
            self._gpio.setup(self._controlGPIOs[gpio],self._gpio.OUT, initial=0)

        self._speedGpioL = self._gpio.setup(25,self._gpio.OUT )
        self._speedGpioL =  self._gpio.PWM(25, 200) #Pin 25 for speed control L and using 200 hz

        self._speedGpioR = self._gpio.setup(26,self._gpio.OUT )
        self._speedGpioR =  self._gpio.PWM(26, 200) #Pin 26 for speed control R and using 200 hz
        self._currrentSpeedL = 0
        self._currrentSpeedR = 0
        self._speedGpioL.start(self._currrentSpeedL)
        self._speedGpioR.start(self._currrentSpeedR)

    def setMotion(self, rotationspeed, frontSpeed):
        self._currrentSpeedL = (frontSpeed - rotationspeed)/2
        self._currrentSpeedR = (frontSpeed + rotationspeed)/2

        if self._currrentSpeedL < 0:
            self._controlStates['LeftRev']= True
        else:
            self._controlStates['LeftRev']= False

        if self._currrentSpeedR < 0:
            self._controlStates['RightRev'] = True
        else:
            self._controlStates['RightRev'] = False

        self._speedGpioL.ChangeDutyCycle(abs(self._currrentSpeedL))
        self._speedGpioR.ChangeDutyCycle(abs(self._currrentSpeedR))


        for state in self._controlStates:
            #Set gpios according to current states...
            #print state, self._controlGPIOs[state],  self._controlStates[state]
            self._gpio.output(self._controlGPIOs[state], self._controlStates[state])

    def getCurrent(self):
        return self._controlStates, self._currrentSpeedL, self._currrentSpeedR



if __name__ == '__main__':
    print "Testcode for Driver"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    import time
    mc= MotorControlL298(GPIO)
    mc.setMotion(0,100)
    print mc.getCurrent()
    time.sleep(2)
    mc.setMotion(50,100)
    print mc.getCurrent()
    time.sleep(2)
    mc.setMotion(-50,100)
    time.sleep(2)
    mc.setMotion(-50,-100)
    time.sleep(2)
    print mc.getCurrent()
    GPIO.cleanup()
