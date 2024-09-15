from time import time
import cv2 as cv
import numpy as np
from windowCapture import WindowCapture
from vision import Vision

# loading images
base = "base.png"
frog = "./targets/frog.png"
ball_red = "./targets/balls/ball-red.png"
ball_pink = "./targets/balls/ball-pink.png"
ball_yellow = "./targets/balls/ball-yellow.png"
ball_green = "./targets/balls/ball-green.png"
ball_blue = "./targets/balls/image.png"

capture = WindowCapture('Zuma Deluxe 1.0')
vision = Vision(ball_blue)
vision.init_control_gui()

loop_time = time()
while(True):
  screenshot = capture.get_screenshot()

  #rectangles = vision.findTarget(screenshot, 0.45, (255,0,255))
  #output = vision.drawTarget(screenshot, rectangles, 'rectangle')

  output = vision.apply_hsv_filter(screenshot)
  cv.imshow('Output', output)

  print('FPS {}'.format(1 / (time() - loop_time)))
  loop_time = time()

  if cv.waitKey(1) == ord('q'):
    break
cv.destroyAllWindows
