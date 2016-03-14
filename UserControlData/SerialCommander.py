import serial
import struct

class SerailCommander:
    def __init__(self):
        self.ser = serial.Serial(
              port='/dev/ttyAMA0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
    def sendSerialCommand(self,speed,turn):
        string = 't'
        string += struct.pack('!B',turn)
        string += 's'
        string += struct.pack('!B',speed)
        self.ser.write(string)





if __name__ == '__main__':
    ser = SerailCommander()
    while 1:
        i1 = input('Turn: ')
        i2 = input('Speed: ')
        ser.sendSerialCommand(i2, i1)
