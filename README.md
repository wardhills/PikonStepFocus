# PikonStepFocus
Pikon telescope with stepper motor focusing mechanism

This project is a fork of the Pikon telescope by Mark Wrigely at Alternative-Photonics ( https://pikonic.com/).  The Pikon is a very accessible and easy to build Newtonian telescope with 3D printed parts. 

I built one when it was first released and had some good images of the moon from it.  However, I found that the time to focus was about on the same order as the time it took for the moon to move out of view.  Translating the telescope to follow the moon disrupted the focus. 

Motorised focusing would all both speed and consistency.  A quick prototype was constructed using a carriage from a CD player to move the raspberrypi camera. It worked, but suffered in several ways, first the simple dc motor did not move forward and backward symmetrically the telescope tube was in near vertical orientations.  It moves downward more easily than upward.  The second was a lager and more obvious problem.  The camera and carriage assembly was large, blocked light and distorted the image.

A stepper motor was chosen for the next iteration.  The spider was redrawn to hold the motor and a slider to hold the camera.  


# Components 
Spider
	ring
	veins 
	motor mount
slider (camera mount)
Motor driver
RaspberryPi
Battery 
Cables 

Note: This project has passed through several iterations.  The condition of the code is far from ideal.   What is posted in this initial release is the first working version which still contains much of the early code commented our for internal reference.  The intention is to remove all of the development code but getting the repo posted was a higher priority. 

# Dependencies 
    • Python 3x
    • Pygame 
    • RPi.GPIO 0.6.3
    • RpiMotorLib (https://github.com/gavinlyonsrepo/RpiMotorLib/) 

# TODO
Describe raspberrypi, A4988 stepper motor control board and power circuit board.
Overview of the project 
Add photos to this ReadME
