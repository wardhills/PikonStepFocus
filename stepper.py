#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2018  Ward Hills


import RPi.GPIO as GPIO
import time

# Variables

delay = 0.0055

steps = 100

pause = 0
cntr =0

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

# Enable GPIO pins for  ENA and ENB for stepper

enable_a = 18
enable_b = 22

# Enable pins for IN1-4 to control step sequence

coil_A_1_pin = 23
coil_A_2_pin = 24
coil_B_1_pin = 4
coil_B_2_pin = 17

# Set pin states
def set_pins():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(enable_a, GPIO.OUT)
  GPIO.setup(enable_b, GPIO.OUT)
  GPIO.setup(coil_A_1_pin, GPIO.OUT)
  GPIO.setup(coil_A_2_pin, GPIO.OUT)
  GPIO.setup(coil_B_1_pin, GPIO.OUT)
  GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Set ENA and ENB to high to enable stepper

#GPIO.output(enable_a, True)
#GPIO.output(enable_b, True)

# Function for step sequence

def setStep(w1, w2, w3, w4):
  GPIO.output(enable_a, True)
  GPIO.output(enable_b, True)
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

# loop through step sequence based on number of steps

def move_forward(steps, delay=0.0055, pause=0, cntr=0):
  print("forward ",steps," Steps, with delay of", delay)
  set_pins()

  for i in range(0, steps):
      setStep(1,0,1,0)
      time.sleep(delay)
      setStep(0,1,1,0)
      time.sleep(delay)
      setStep(0,1,0,1)
      time.sleep(delay)
      setStep(1,0,0,1)
      time.sleep(delay)
      cntr = cntr +1 
      print(cntr)
      time.sleep(pause)
  GPIO.cleanup()

# Reverse previous step sequence to reverse motor direction
def move_reverse(steps, delay=0.0055, pause=0, cntr=0):
  print("reverse ",steps," Steps, with delay of", delay)
  set_pins()

  for i in range(0, steps):
      setStep(1,0,0,1)
      time.sleep(delay)
      setStep(0,1,0,1)
      time.sleep(delay)
      setStep(0,1,1,0)
      time.sleep(delay)
      setStep(1,0,1,0)
      time.sleep(delay)
      cntr = cntr -1
      print(-cntr)
      time.sleep(pause)
  GPIO.cleanup()

def cleanup():
  GPIO.cleanup()

if __name__ == '__main__':
  try:
    print('Command letter followed by number');
    print('p20 - set the inter-step period to 20ms (control speed)');
    print('f100 - forward 100 steps');
    print('r100 - reverse 100 steps');
    
    while True:      # (4)
        command = raw_input('Enter command: ')
        parameter_str = command[1:] # from char 1 to end
        parameter = int(parameter_str)     # (5)
        if command[0] == 'p':     # (6)
            #period = parameter / 1000.0
            delay = parameter / 1000.0
        elif command[0] == 'f':
            move_forward(parameter, delay)
        elif command[0] == 'r':
            move_reverse(parameter, delay)
  finally:
      print('Cleaning up')
      GPIO.cleanup()



    
  

  

