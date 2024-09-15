from time import time
import cv2 as cv
import numpy as np
from windowCapture import WindowCapture

'''
def draw_rectangle(base, target, rectangle, color):
  needle_w = target.shape[1]
  needle_h = target.shape[0]
  line_color = color
  line_type = cv.LINE_4

  top_left = (rectangle[0], rectangle[1])
  bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
  cv.rectangle(base, top_left, bottom_right, line_color, line_type)
'''

# def findCenterPoint(haystack_path, needle_path, threshold, color):
#   haystack = cv.imread(haystack_path, cv.IMREAD_UNCHANGED)
#   needle = cv.imread(needle_path, cv.IMREAD_UNCHANGED)

#   needle_w = needle.shape[1]
#   needle_h = needle.shape[0]

#   result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)

#   locations = np.where(result >= threshold)
#   locations = list(map(lambda loc: (int(loc[0]), int(loc[1])), zip(*locations[::-1])))

#   rectangles = []
#   for location in locations:
#     rect = [int(location[0]), int(location[1]), needle_w, needle_h]
#     rectangles.append(rect)
#     rectangles.append(rect)

#   rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
#   print(rectangles)

#   points = []
#   if len(rectangles):
#     for rect in rectangles:
#       center_x = rect[0] + needle_w // 2
#       center_y = rect[1] + needle_h // 2
      
#       points.append((center_x, center_y))

#       cv.drawMarker(haystack, (center_x, center_y), color, cv.MARKER_CROSS, 25, 2, cv.LINE_8)

#     cv.imshow("Result", haystack)
#     cv.waitKey()

#   formatted_points = [(int(point[0]), int(point[1])) for point in points]
#   return formatted_points

# # loading images
# base = "base.png"
# frog = "./targets/frog.png"
# ball_red = "./targets/balls/ball-red.png"
# ball_pink = "./targets/balls/ball-pink.png"
# ball_yellow = "./targets/balls/ball-yellow.png"
# ball_green = "./targets/balls/ball-green.png"
# ball_blue = "./targets/balls/ball-blue.png"

# points = findCenterPoint(base, ball_yellow, 0.64, (0, 0, 255))
# print(points)

capture = WindowCapture('Zuma Deluxe 1.0')

loop_time = time()
while(True):
  screenshot = capture.get_screenshot()

  cv.imshow("Screenshot", screenshot)

  print('FPS {}'.format(1 / (time() - loop_time)))
  loop_time = time()

  if cv.waitKey(1) == ord('q'):
    break

cv.destroyAllWindows


