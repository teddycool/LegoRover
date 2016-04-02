import os
import sys

import time
from UserControlData import UserControlData
from SerialCommander import SerailCommander
from threading import Thread, Lock


path = "/home/pi/named_pipe.fifo"
#os.mkfifo(path)  # TODO setup fifo file if needed



class UserControlReciver:

    def __init__(self):
        self.user_data = UserControlData()
        self.mutex = Lock()

    def read_fifo(self):

        print "file opened"
        while self.user_data.run:
            fifo = open(path,"r")
            for line in fifo:
                 print "Back end received: " + line
                 self.mutex.acquire()
                 self.user_data.readInputString(line)
                 self.mutex.release()
            fifo.close()
        print "Ending read fifo"

    def start_fifo(self):

        p = Thread(target = self.read_fifo, args = ())
        p.start()




if __name__ == '__main__':
    r = UserControlReciver()
    r.start_fifo()
    ser = SerailCommander()
    while 1:
        r.mutex.acquire()
        #print "Data is : " + r.user_data.data
        #print "Speed is : " + str(r.user_data.speed)
        #print "Turn is : " + str(r.user_data.turn)
        ser.sendSerialCommand(r.user_data.speed, r.user_data.turn)
        r.mutex.release()
        time.sleep(0.1)
