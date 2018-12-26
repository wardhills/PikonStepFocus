#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  TelescpCtrl.py
#
#  Copyright 2018  Ward Hills

# STREAMS VIDEO FROM CAMERA and CONTROLS POSITION OF SENSOR

# RUNS UNDER: gksudo idle via ssh

# Run instructions
# on raspbian distro headless over ssh via putty:
# needs xwindows server running on windows
#  ssh -Y  IPaddr   on Linux
# from the command line run: gksudo python telescp_cntrl.py
# Sensor window needs to be the active window for key commands to function

import sys                  # for cleanup
import time
import datetime
import io
import pygame
from pygame.locals import *
# import stepper
import camexpsr
from RpiMotorLib import RpiMotorLib
import RPi.GPIO as GPIO

try:
    print("Starting picamera")
    import picamera
except Exception as E:
    print(E)
    print("Picamera not reachable, continuing with out it")

# ---Hardware configuration-----------------------------------------
""" if certain items of hardware are not present functions can result i errors """
# TODO add flags to activate a test (with out HW mode) and active mode
# use error trapping

# Image parameters
# for full visiability on Rpi 7 inch touch screen
# x_pixels = 640
# y_pixels = 480

x_pixels = 1280
y_pixels = 960

# max resolutuon of Rpi v1 camera, too large for 7 inch screen
# x_pixels = 2592
# y_pixels = 1944

iso_values = [100, 200, 320, 400, 500, 640, 800]

# ---PYGAME SETUP--------------------------------------------
# Set up for Rpi 7 inch touch screen
# Viewable screen size: 155mm x 86mm
# Screen Resolution 800 x 480 pixels


def pygame_setup(x_size=320, y_size=240, caption_text='Telescope'):
    pygame.init()
    screensize = (x_size, y_size)
    pygame.display.set_mode(screensize, pygame.RESIZABLE)
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption(caption_text)
    return screen
# ---End Pygame setup---------------------------------------

# ---Motor set up--------------------------------------------
# Set GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO_pins = (14, 15, 18)         # Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 20                   # Direction -> GPIO Pin
step = 21                        # Step -> GPIO Pin
sleep = 16                       # GPIO Pin held low by default; a low-powered sleep mode to consume minimal current.

# the A4988 board is a low current state if the Sleep pin is set low
#  The sleep pin on the A4988 board is puled up to "High" on startup with a pull up resistor to the logic voltage pin

GPIO.setup(sleep, GPIO.OUT)     # set the mode of the pin to "OUT"


def motor_wake(pin=16, state=1):
    if state == 1:
        GPIO.output(pin, GPIO.HIGH)     # wake the motor
    elif state == 0:
        GPIO.output(pin, GPIO.LOW)      # sleep the motor
    # print("expected 0 to sleep or 1 to wake motor.  Got :",state)
    return state                        # can be used to query wake state of motor


def set_steptype():
    steptypes = ['Full', 'Half', '1/4', '1/8', '1/16']
    for i in range(0, len(steptypes)):
        print(i, " - ", steptypes[i])
    choice = int(input('press 1 to 4 to choose steptype'))
    steptype = str(steptypes[choice])
    return steptype
# ---End Motor setup--------------------------------------------


# ---SYSTEM FUNCTIONS---------------------------------------
def cleanup():
    camera.close()
    GPIO.cleanup()
    pygame.display.quit()
    pygame.quit()
    sys.exit()
# ---End System functions-----------------------------------

# ---motor control------------------------------------------


steps = 1   # number of steps taken by motor


# ---End motor control

def image_capture(c, images_number=1):
    time.sleep(2)
    for i in range(images_number):
        timestamp = datetime.datetime.now().isoformat()
        c.capture(timestamp+'.jpg')
        time.sleep(1)


def menu_text():
    print('up arrow - further away')
    print('arrow - closer')
    print('right - larger step')
    print('left  - smaller step')
    print('space - step to 1')
    print('c     - capture current image')
    print('v     - capture video')
    print('e     - ramp exposures')
    print('i     - change iso')
    print('sft f - decrease frame rate')
    print('f     - increase frame rate')
    print('m     - menu')
    return


if __name__ == "__main__":
    try:
        print('start pygame')
        screen = pygame_setup(x_pixels, y_pixels)

        menu_text()
        print('Enter a comand')
        
# TODO can scroll bars be added?
        while True:
            with picamera.PiCamera() as camera:
                camera.led = False
                camera.resolution = (x_pixels, y_pixels)
                # Low framerates can cause over exposure
                camera.framerate = 15      # 1/6 (0.1666) fps to max of 15fps
                camera.preview_alpha = 0
                camera.iso = 100
                camera.start_preview()
                stream = io.BytesIO()

                # ---Capture stream and send to pygame window
                print('Starting stream')
                # "stream" is the abr name for the string output of the capture

                for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
                    stream.truncate()
                    stream.seek(0)
                    stream_copy = io.BytesIO(stream.getvalue())
                    image = pygame.image.load(stream_copy, 'jpg').convert()
                    video = screen.blit(image, (0, 0))
                    pygame.display.update(video)

# TODO: add the camera position to the graphical display
                    # ---Display Camera position
                    # try:
                    #     #print("Camera position : %.1f" % camera_position)
                    #     w = screen.get_width() - 20
                    #     h = pygame.display.Info().current_h - 20
                    #     proximity = (camera_position / camera_position_max) * h
                    #     if proximity < 1:
                    #         proximity = 1
                    #     pygame.display.update(pygame.draw.rect(screen, (225, 0, 0), Rect((10, 3), (3, proximity))))
                    #     pygame.display.update(video)
                    # except Exception as E:
                    #     #print(E)
                    # --- Move Camera

# instantiate the motor object and pass the identities of the GPIO pins
                    mymotor = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
                    steptype = 'Full'  # defalut step size
                    steps = 1  # default number of steps

                    for event in pygame.event.get():

                        if event.type == QUIT:
                            sys.exit()
                        if event.type == KEYDOWN:
                            if event.key == K_UP:
                                motor_wake(sleep, 1)  # wake the motor
                                mymotor.motor_go(True, steptype, steps, .01, Tsrue, .05)
                                motor_wake(sleep, 0)  # sleep the motor

                            elif event.key == K_DOWN:
                                motor_wake(sleep, 1)  # wake the motor
                                mymotor.motor_go(False, steptype, steps, .01, True, .05)
                                motor_wake(sleep, 0)  # sleep the motor

                            elif event.key == K_RIGHT:
                                steps = steps + 1
                                if steps >= 200:
                                    steps = 200
                                    print('max number of steps per press is 200')
                                print('steps taken per key press: ', steps)

                            elif event.key == K_LEFT:
                                steps = steps - 1
                                if steps <= 1:
                                    steps = 1
                                    print('min number of steps per press is 1')
                                print('steps taken per key press: ', steps)

                            elif event.key == K_SPACE:
                                steps = 1
                                print('steps taken per key press: ', steps)
                                pass

                            elif event.key == K_c:
                                # camera.resolution = (2592, 1944)               # Rpi V1 at max resolution
                                camera.resolution = (3280, 2464)               # Rpi V2 at max resolution
                                print('resolution set to ', camera.resolution)
# TODO  The capture should be moved to a function callable at this point
                                images_number = 20                          # number of images captured
# TODO add adjustment to framerate to avoid over exposure
                                time_stamp = time.strftime("%Y%m%d_%H%M%S")  # TODO change to ISO format
                                print('started at ', time_stamp)
                                camera.framerate = 15      # 1/6 (0.1666) fps to max of 15fps
                                print('framerate ', camera.framerate)
                                # camera.capture_sequence(['img'+time_stamp+'%2d.jpg' % i for i in range(0, images_number)], splitter_port=0, use_video_port=False)
                                # camera.capture_sequence(['img'+time_stamp+'%2d.bmp' % i for i in range(0, images_number)], splitter_port=0, format='bmp', use_video_port=False)
# TODO sethe path where the data is stored in a user varable defined at the start of the programme
                                camera.capture_sequence(['../Telescope_data/'+time_stamp+'%2d.bmp' % i for i in range(0, images_number)], splitter_port=0, format='bmp', use_video_port=False)
                                print('CAPTURE ', images_number,'Images')
                                camera.resolution=(x_pixels,y_pixels)
                                print('Ended at ', time_stamp)

                                print('returning resolution to ', x_pixels, y_pixels)
                                camera.capture_continuous(stream, format='jpeg', use_video_port=True)
                                print('returning to continuous capture')

                            elif event.key == K_v:
                                # camexpsr.cptr_vid(camera,time=60, x=1280,y=960)
                                camexpsr.cptr_vid(camera,time=60, x=1296,y=972)
                                print('returning to continuous captute')
                                camera.capture_continuous(stream, format='jpeg', use_video_port=True)
                              
                            elif event.key == K_e:
                                # camera.resolution=((2592,1944))
                                camera.resolution = (3280, 2464)               # Rpi V2 at max resolution
                                camexpsr.ramp(camera)
                                camera.resolution = (x_pixels, y_pixels)

                                print('returning resolution to ', x_pixels, y_pixels)
                                camera.resolution =(x_pixels, y_pixels)
                                camera.capture_continuous(stream, format='jpeg', use_video_port=True)
                                print('returning to continuous capture')

                            elif event.key == K_f:
                                if pygame.key.get_mods() & KMOD_SHIFT:
                                    camera.framerate = camera.framerate + 1
                                camera.framerate = camera.framerate - 1
                                print("camera.framerate = ", camera.framerate)

                            elif event.key == K_i:
                                camera.iso = input(" enter iso value, 100, 200, 320, 400, 500, 640, or 800 ")
                                print("iso = ", camera.iso)

                            elif event.key == K_m:
                                menu_text()

    except Exception as E:                                      # capture and print any error and clean up
        print(E)
        cleanup()