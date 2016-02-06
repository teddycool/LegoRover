__author__ = 'teddycool'
#Handles the actual motors
from IMotionControl import IMotionControl


class MotorControlL298(IMotionControl):

    def __init__(self, GPIO):
        super(MotorControlL298, self).__init__()
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

    def setMotion(self, rotationspeed, frontSpeed):
        print "MotorControlL298 setMotion..."
        return


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
    mc= MotorControlL298(GPIO)
    speed =100
    mc.setSpeed(speed)
    mc.forward()
    while speed > 0:
        time.sleep(3)
        speed =speed - 10
        mc.setSpeed(speed)
        print mc.getCurrent()
    mc.stop()
    print mc.getCurrent()
    GPIO.cleanup()
