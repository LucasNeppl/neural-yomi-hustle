import keyboard
from mss import MSS
import cv2
import numpy as np
import pyautogui
import time
import math

class WindowCapture:
    def __init__(self, target_Window):
        self.window = target_Window
        self.scale_x = target_Window["width"] / 1920 #For example if window is 960x540 then scale_x = 0.5 and scale_y = 0.5
        self.scale_y = target_Window["height"] / 1080
        self.sct = MSS()
        

    def getGray(self): #Format raw_frame[y][x][0]
        return cv2.cvtColor(self.getRaw(), cv2.COLOR_BGR2GRAY)

    def getRaw(self): #Format raw_frame[y][x][0]
        return np.array(self.sct.grab(self.window))    
    
    def getScale(self):
        return self.scale_x, self.scale_y
    
    def getWindow(self):
            return self.window

    
    