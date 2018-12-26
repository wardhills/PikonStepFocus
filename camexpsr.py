#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  camexpsr.py
#
#  Copyright 2018  Ward Hills
 #code based on https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-in-low-light

from picamera import PiCamera
from time import sleep
from fractions import Fraction
import datetime
import sys

# Force sensor mode 3 (the long exposure mode), set
# the framerate to 1/6fps, the shutter speed to 6s,
# and ISO to 800 (for maximum gain)
# the maximum n/d value is 6 sec V1 Rpicam, 10 for V2
# Set resolution:
#for Camera V1
px = 2592
py = 1944

#for Camera V2
#px = 3280
#py = 2464

def create(fps=15, px=2592, py=1944):
    # create a camera with defalt values for a long  exposure. Takes frame rate as a float
    try:
       Cam = PiCamera(
            resolution=(px, py),
            framerate=fps,
            sensor_mode=3, splitter_port=2)
       print("created camera",PiCamera)

    except Exception as e:
        print(e)
        return

    return Cam

def framerateset(c,fps=0.5, iso=800, eq_time=5):
    c.framerate = fps
    print ('Framerate set to :',c.framerate)
    c.shutter_speed = 6000000
    c.iso = iso
    sleep(eq_time)  # 10 sec seems to be sufficient for dark sky
    c.exposure_mode = 'off'
    return camera

def framerateset_fract(c,numer=1, dmntr=6,iso=800, eq_time=3):
    c.framerate=Fraction(numer, dmntr)
    print ('Framerate set to :',c.framerate)
    c.shutter_speed = 6000000
    c.iso = iso
    sleep(eq_time)  # 10 sec seems to be sufficient for dark sky 
    c.exposure_mode = 'off'
    return c

def cptr(c):
    timestamp=datetime.datetime.now().isoformat()
    #cptr_name =(timestamp+'.jpg')    #  this format works
    #cptr_name =(timestamp+'.rgba')   #  rgba formatt does not work; can not determin format 
    cptr_name =(timestamp+'.bmp')
    c.capture(cptr_name, 'bmp')
    print("captured image: ",timestamp)
    print("at Framerate :",c.framerate)
    return cptr_name


def ramp(c, lngst = 0.5, shrst = 15, nmbr_img  = 5):
    #  lngst = 0.16666
    framerate = 0
    #lngst - in frames per second (fps) the longest exposure time
    #shrst - in fps the shorest exposire time.   0.067 = 15 fps

    #determine the step size in exposure time (1/s) to get an even range of exposures
    #calculate the range of exposures in 1/s
    lngst_exposure = 1/lngst      #sec
    shrst_exposure = 1/shrst      #sec
    range_exposure = lngst_exposure-shrst_exposure 
    print('range :',range_exposure)
    step = range_exposure/(nmbr_img) #s

    exposure = lngst_exposure  #sec  initailly set the exposure at the longest 

    print('capturing ', nmbr_img , 'images from ', lngst_exposure , ' to ',  shrst_exposure, 'sec exposure')
    print('-------------------/')

    #for i in range(0, nmbr_img):
    
    try:
        while framerate <=shrst:
            framerate = 1/exposure   #1/s
            print ('framerate', framerate)
            dmntr  = 6  *10000    # using 6 as the fixe demonator because the longest esposure on the camera is 6 sec
            numer = int(round(framerate * dmntr,0))
            print('capturing at ', round(framerate,3),' fps or' , round(exposure,3) ,' sec exposure ')
            c.framerate = Fraction(numer, dmntr)
            #print("c.framerate : ",c.framerate)
            file_name = cptr(c)
            print(file_name)
            exposure = exposure - step  #s
            if exposure <= 1/shrst:
                return

    except Exception as e:
        print(e)

    finally:
        return

def cptr_vid(c,time=60, x=640,y=480):
    print('recording video')
    timestamp=datetime.datetime.now().isoformat()
    c.resolution = (x,y)
    print('capturing at', x ,',', y)
    print('Capturing for ',time,'s')
    cptr_name =(timestamp+'.h264')
    c.start_recording(cptr_name, format='h264', quality=5)
    c.wait_recording(time)
    c.stop_recording()

    
            

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            n = int(sys.argv[1])  # passes the first parm to the variable
            d = int(sys.argv[2])
        camera = create()                                            # Create a camera instance with default conditions
        cptr_camera = framerateset_fract(c=camera, numer=n, dmntr=d) # set framerate to user defn'd values
        #file_name = cptr(cptr_camera)
        cptr(cptr_camera)

    except Exception as e:
        print(e)
        print("the framerate can be set by adding the Numerator and Demonator arguments. e.g. python camexpsr.py 1 6 . Using default framerate values")
#        camera.close()                                     # kill any instance created that is associated with the error
        camera = create()                                  # creates a fresh instance of the camera
#        ramp_fract(camera)
        cptr_vid(camera,time=10)

        camera.close()                                     # clean up
        
