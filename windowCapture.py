import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:  
  hwnd = None

  def __init__(self, window_name):
    self.hwnd = win32gui.FindWindow(None, window_name)
    if not self.hwnd:
      raise Exception('Window not found')

  def get_screenshot(self):
    rect = win32gui.GetWindowRect(self.hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    wDC = win32gui.GetWindowDC(self.hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(self.hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]
    img = np.ascontiguousarray(img)

    return img
