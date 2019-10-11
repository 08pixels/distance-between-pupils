from imutils import face_utils
from pupil_distance import *
import numpy as np
import argparse
import imutils
import dlib
import cv2
import time
# construct the argument parser and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument('-p', '--shape-predictor', required=True,
                help='path to facial landmark predictor')
ap.add_argument('-i', '--image', required=True,
                help='path to input image')
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args['shape_predictor'])

# load the image, resize it, and conver it to grayscale
image = cv2.imread(args['image'])
# image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
rects = detector(gray, 1)

# loop over the face detections
for (i, rect) in enumerate(rects):
  # determine the facial landmarks for the face region, then
  # convert the facial landmark (x, y)-coordinates to a NumPy
  # array
  shape = predictor(gray, rect)
  shape = face_utils.shape_to_np(shape)

  # convert dlib's retangle to a OpenCV-style bounding box
  # [i.e., (x, y, w, h)], then draw the face bounding box
  (x, y, w, h) = face_utils.rect_to_bb(rect)
  cv2.rectangle(image, (x,y), (x + w, y + h), (0, 255, 0), 2)

  # show the face number
  cv2.putText(image, 'Face #{}'.format(i + 1), (x - 10, y - 10),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

  # loop over the (x, y)-coordinates for the facial landmarks
  # and draw them on the image
  for (j, (x, y)) in enumerate(shape):
    if(j in [37, 38, 40, 41, 43, 44, 46, 47]):
      cv2.circle(image, (x, y), 1, (255, 0, 0), -1)
    else:
      cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

  # estimating pupil center from known points 
  left_pupil = Pupil(shape[37], shape[40],
      shape[41], shape[38]).central_point

  right_pupil = Pupil(shape[43], shape[46],
      shape[47],shape[44]).central_point
  
  # drawing the lines to find the pupil
  for ((a, b), (c, d)) in [(shape[37], shape[40]), (shape[38], shape[41]), (shape[43], shape[46]), (shape[47], shape[44])]:
    cv2.line(image,
            (a, b),
            (c, d),
            (255,0,0), 1)

  # drawing central points and showing informations
  cv2.circle(image, (int(left_pupil.x), int(left_pupil.y)), 1, (0, 0, 255), -1)
  cv2.circle(image, (int(right_pupil.x), int(right_pupil.y)), 1, (0, 0, 255), -1)

  cv2.line(image,
          (int(left_pupil.x), int(left_pupil.y)),
          (int(right_pupil.x), int(right_pupil.y)),
          (0,0,255), 1)

  pupil_distance = Pupil.distance(left_pupil, right_pupil)
  cv2.putText(image, 'distance: {:.2f} px'.format(pupil_distance), (int(left_pupil.x), int(left_pupil.y - 5)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

# show the output image with the face detection + facial landmarks
# cv2.imshow('Output', image)
# cv2.waitKey(0)

cv2.imwrite('output/{}.jpg'.format(time.time()), image)
