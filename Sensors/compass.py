__author__ = 'teddycool'

#http://think-bowl.com/raspberry-pi/i2c-python-library-3-axis-digital-accelerometer-adxl345-with-the-raspberry-pi/
#http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html

import smbus
import time
import math
import cv2
from config import roverconfig



class Compass(object):

    def __init__(self, bus = 1, address = 0x1e):
        self._bus = smbus.SMBus(bus)
        self._address = address
        self._compass = (0,0,0)
        self._bearing = 0
        return

    def initialize(self, degrees=0, minutes=0):
        #TODO: Set calibration-values from config...
        self._write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
        self._write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
        self._write_byte(2, 0b00000000) # Continuous sampling
        return


    def update(self):
        self._x_out = (self._read_word_2c(3) + roverconfig["Compass"]["OffsetX"]) * roverconfig["Compass"]["Scale"]
        self._y_out = (self._read_word_2c(7) + roverconfig["Compass"]["OffsetY"])* roverconfig["Compass"]["Scale"]
        self._z_out = self._read_word_2c(5) * roverconfig["Compass"]["Scale"]
        self._compass=(round(self._x_out,1), round(self._y_out,1), round(self._z_out,1))
        self._bearing  = math.atan2(self._y_out, self._x_out)
        if (self._bearing < 0):
            self._bearing += 2 * math.pi
        self._bearing = round(self._bearing,1)
        print "Bearing: " + str(self._bearing)
        return self._bearing

    def draw(self, frame, textstartx, textstarty):
        #Draw compass values on screen...
        cv2.putText(frame, "Bearing: " + str(self._bearing), (textstartx,textstarty),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame

    def _read_byte(self,adr):
        return self._bus.read_byte_data(self._address, adr)

    def _read_word(self,adr):
        high = self._bus.read_byte_data(self._address, adr)
        low = self._bus.read_byte_data(self._address, adr+1)
        val = (high << 8) + low
        return val

    def _read_word_2c(self, adr):
        val = self._read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def _write_byte(self,adr, value):
        self._bus.write_byte_data(self._address, adr, value)


if __name__ == '__main__':
    print "Testcode for compass"
    from config import roverconfig
    cp = Compass()
    cp.initialize()
    while True:
        cp.update()
        print "Bearing: " + str(cp._bearing) + "X, Y: " + str(cp._x_out) + ", " + str(cp._y_out) + "Compass: " + str(cp._compass)
        time.sleep(0.2)

