# USAGE
# python detect_bright_spots.py --image images/lights_01.png

""" this code is based on code provided by Pyimagesearch  (https://www.pyimagesearch.com)  """


#TODO  convert to a library structure with functions and main
#TODO document logic flow out of and into telescope controler 1 capture initial image 2) find bright spots 3) crop around and store pixel area
# 4) measure focus 5) capture next image useing only cropped area, 6) measure focus 7) adjust focus 8) GOTO 5)
# TODO learn how to capture from a defined part of thr Rpi v2 camera sensor


# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the image file")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# threshold the image to reveal light regions in the
# blurred image
# thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.threshold(blurred, 25, 32, cv2.THRESH_BINARY)[1]
#print('thresh shape :',thresh.shape)

# perform a series of erosions and dilations to remove
# any small blobs of noise from the thresholded image
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=4)

# perform a connected component analysis on the thresholded
# image, then initialize a mask to store only the "large"
# components
labels = measure.label(thresh, neighbors=8, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")
#print('labels ', labels)

# loop over the unique components
for label in np.unique(labels):
	# if this is the background label, ignore it
	if label == 0:
		continue

	# otherwise, construct the label mask and count the
	# number of pixels 
	labelMask = np.zeros(thresh.shape, dtype="uint8")
	labelMask[labels == label] = 255
	numPixels = cv2.countNonZero(labelMask)

	# if the number of pixels in the component is sufficiently
	# large, then add it to our mask of "large blobs"
	if numPixels > 300:
		mask = cv2.add(mask, labelMask)

# find the contours in the mask, then sort them from left to
# right
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
#print('cnts :',cnts)
cnts = imutils.grab_contours(cnts)
cnts = contours.sort_contours(cnts)[0]

# loop over the contours
for (i, c) in enumerate(cnts):
	# draw the bright spot on the image
	(x, y, w, h) = cv2.boundingRect(c)
	((cX, cY), radius) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(cX), int(cY)), int(radius),
		(0, 0, 255), 3)
	cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)


#if the image is too large to show on the screen it can be resized
# we need to keep in mind aspect ratio so the image does
# not look skewed or distorted -- therefore, we calculate
# the ratio of the new image to the old image
num = 1000
r = num / image.shape[1]
dim = (num, int(image.shape[0] * r))

# perform the actual resizing of the image and show it
# this is only need if the image is too large for the screen to show
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("resized", resized)
cv2.waitKey(0)

print(x,y,w,h)

#scale the rectangle to the new size of the image
x,y,w,h = int(x * r), int(y * r), int(w * r), int(h * r)


print(x,y,w,h)
# maintain maximum resolution the input x,y,w,h should be the output of the countour finding function above, not scaled
# initially this code assumes there is only one bright object found in the frame.
# Corners of cropped rectangle
padding = 100  # number of pixels around the edges of the bright spot
x1 = x - padding
x2 = x + w + padding
y1 = y + padding
y2 = y - h - padding

print(x1,x2,y1,y2)

# crop the image using array slices -- it's  a NumPy array
# after all!
#cropped = resized[70:170, 440:540]
cropped = resized[y2:y1,x1:x2]
cv2.imshow("cropped", cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()