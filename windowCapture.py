import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:  
  hwnd = None
  w = 0
  h = 0
  cropped_x = 0
  cropped_y = 0
  offset_x = 0
  offset_y = 0


  def __init__(self, window_name):
    self.hwnd = win32gui.FindWindow(None, window_name)
    if not self.hwnd:
      raise Exception('Window not found')
    
    rect = win32gui.GetWindowRect(self.hwnd)
    x = rect[0]
    y = rect[1]
    self.w = rect[2] - x    
    self.h = rect[3] - y

    titlebar_pixels = 26
    border_pixels = 4
    self.w = self.w - (border_pixels * 2)
    self.h = self.h - titlebar_pixels - border_pixels
    self.cropped_x = border_pixels
    self.cropped_y = titlebar_pixels

    self.offset_x = x + self.offset_x
    self.offset_y = y + self.cropped_y

  def get_screenshot(self):

    wDC = win32gui.GetWindowDC(self.hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (self.h, self.w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(self.hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]
    img = np.ascontiguousarray(img)

    return img
  
  def get_screen_position(self, pos):
    return (pos[0] + self.offset_x, pos[1] + self.offset_y)
