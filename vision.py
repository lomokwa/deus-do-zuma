import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter

class Vision:
  TRACKBAR_WINDOW = "Trackbars"

  method = None
  needle = None
  needle_w = 0
  needle_h = 0

  def __init__(self, needle_path, method=cv.TM_CCOEFF_NORMED):
    self.needle = cv.imread(needle_path, cv.IMREAD_COLOR)
    self.needle_w = self.needle.shape[1]
    self.needle_h = self.needle.shape[0]

    self.method = method

  def draw_rectangle(self, base, rectangle, color):
    line_color = color
    line_type = cv.LINE_4

    top_left = (rectangle[0], rectangle[1])
    bottom_right = (top_left[0] + self.needle_w, top_left[1] + self.needle_h)
    cv.rectangle(base, top_left, bottom_right, line_color, line_type)


  def findTarget(self, haystack_img, threshold, color, debug=None):
    result = cv.matchTemplate(haystack_img, self.needle, self.method)

    threshold = float(threshold)

    locations = np.where(result >= threshold)
    locations = list(map(lambda loc: (int(loc[0]), int(loc[1])), zip(*locations[::-1])))

    rectangles = []
    for location in locations:
      rect = [int(location[0]), int(location[1]), self.needle_w, self.needle_h]
      rectangles.append(rect)
      rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
    # print(rectangles)

    return rectangles

  def getPoints(self, rectangles):
    points = []
    if len(rectangles):
      for (x, y, w, h) in rectangles:
        center_x = x + w // 2
        center_y = y + h // 2
        
        points.append((center_x, center_y))
    return points
      
  def drawTarget(self, haystack_img, rectangles, debug=None):
    if debug is None:
      points = self.getPoints(rectangles)

      for (center_x, center_y) in points:
        cv.drawMarker(haystack_img, (center_x, center_y), (0, 255, 0), cv.MARKER_CROSS, 25, 2, cv.LINE_8)
      return haystack_img

    elif debug is 'rectangle':
      for (x, y, w, h) in rectangles:
        top_left = (x, y)
        bottom_right = (x + w, y + h)

        cv.rectangle(haystack_img, top_left, bottom_right, (0, 255, 0), cv.LINE_4)
      return haystack_img
    
  def init_control_gui(self):
    cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
    cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

    # This is a required callback
    def nothing(position):
      pass

    # creating trackbars for bracketing
    # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
    cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
    cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
    cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
    # Set default value for Max HSV trackbars
    cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
    cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
    cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

    # trackbars for increasing/decreasing saturation and value
    cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
    cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

  def get_hsv_filter_from_controls(self):
    # Get current positions of all trackbars
    hsv_filter = HsvFilter()
    hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
    hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
    hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
    hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
    hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
    hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
    hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
    hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
    hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
    hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
    return hsv_filter

  def apply_hsv_filter(self, original_img, hsv_filter=None):
    hsv = cv.cvtColor(original_img, cv.COLOR_BGR2HSV)

    if not hsv_filter:
      hsv_filter = self.get_hsv_filter_from_controls()

    h, s, v = cv.split(hsv)
    s = self.shift_channel(s, hsv_filter.sAdd)
    s = self.shift_channel(s, -hsv_filter.sSub)
    v = self.shift_channel(v, hsv_filter.vAdd)
    v = self.shift_channel(v, -hsv_filter.vSub)
    hsv = cv.merge([h, s, v])

    lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
    upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])

    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(hsv, hsv, mask=mask)

    img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
    return img
  
  def shift_channel(self, c, amount):
    if amount > 0:
      lim = 255 - amount
      c[c >= lim] = 255
      c[c < lim] += amount
    elif amount < 0:
      amount = -amount
      lim = amount
      c[c <= lim] = 0
      c[c > lim] -= amount

    return c

