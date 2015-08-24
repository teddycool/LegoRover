__author__ = 'teddycool'

# Put up the camera, run calibrate
# Start to play...
import os, sys, pygame
import picamera
from pygame.locals import *
#from VideoCapture import Device
import pygame.camera
from time import sleep
#import MainLoop
import io
import yuv2rgb

class Main(object):

    def __init__(self):
        print "Init Main object..."
        #Size of application window
        self.dwidth = 640
        self.dheight = 480
        #self._mainLoop=MainLoop.MainLoop()
        self._cam = picamera.PiCamera()
        self._cam.vflip = False
        self._cam.hflip = False
        self._cam.brightness = 60


    def run(self):
        #Init and set up variables...
        print "Init pygame..."
        pygame.init()
        print "Setup screen"
        self.screen = pygame.display.set_mode((self.dwidth,self.dheight))
        #self._mainLoop.initialize()
        self.size=(self.dwidth, self.dheight)
        # Buffers for viewfinder data
        rgb = bytearray(self.dwidth * self.dheight * 3)
        yuv = bytearray(self.dwidth * self.dheight*3/ 2)
        black = 0, 0, 0
        #Init gamestate
        stopped = False
        running=True
        while not stopped:

            # 1 grab image from picamera stream
            # 2 handle image analyze
            # 3 read sensordata (maybe not every frame?
            # 3 use analyze output to control rover
            # 4 publish image with control overlay to video-streamer

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stopped = True
            print "Starting stream"
            stream = io.BytesIO() # Capture into in-memory stream
            self._cam.capture(stream, use_video_port=True, format='raw')
            stream.seek(0)
            stream.readinto(yuv)  # stream -> YUV buffer
            stream.close()
            yuv2rgb.convert(yuv, rgb,self.dwidth,self.dheight)
            print "Image from buffer"
            img = pygame.image.frombuffer(rgb, (self.dwidth,self.dheight), 'RGB')
            self.screen.blit(img, (0, 0))
            pygame.display.update()
            sleep(0.5)
          #  self._mainLoop.update(self.screen)
          #  self._mainLoop.draw(self.screen)

            #pygame.display.flip()

if __name__ == "__main__":
    #Set to webcam ID, std is 0. Networkedcam is probably 1
    #camid=1
    #Set size of screen/window

    gl=Main()
    gl.run()

