import keyboard
from mss import MSS
import cv2
import numpy as np
import pyautogui
import time
import math

from capturewin import WindowCapture
from assets import yomiTXT_NUM, yomiTXT_f

class ComputerVision:
    def __init__(self, target_Window, capture):
        self.capture = capture
        self.window = target_Window
        self.scale_x = target_Window["width"] / 1920 #For example if window is 960x540 then scale_x = 0.5 and scale_y = 0.5
        self.scale_y = target_Window["height"] / 1080
        self.btnpadding = 24 * self.scale_x # how many pixels away from corner to click 24 is middle for default 48x48 buttons also important as pixel differences can add up but only to a small amount
        self.distBtwnBtns = 51 * self.scale_x # how many pixels between buttons



    def getHealth(self, gFrame, lHealth, rHealth):
            leftHealth = lHealth
            rightHealth = rHealth
            y_MidHealthbar = self.window["top"] + math.ceil(self.scale_y * 78) # Roughly middle of healthbar
            x_LeftHealthbarStart = self.window["left"] + math.ceil(self.scale_x * 230) # this includes some padding 
            x_LeftHealthbarEnd = self.window["left"] + math.floor(self.scale_x * 880)
            x_RightHealthbarStart = self.window["left"] + math.floor(self.scale_x * 1680) # note that right's heath bar goes from right to left
            x_RightHealthbarEnd = self.window["left"] + math.ceil(self.scale_x * 1040)
            for x in range(x_LeftHealthbarStart, x_LeftHealthbarEnd): #find first pixel of normal healthbar
                if gFrame[y_MidHealthbar][x] == 204:
                    healthBar = 1-((x-x_LeftHealthbarStart)/(x_LeftHealthbarEnd-x_LeftHealthbarStart))# essentially if it was found 1/4 way through is would set healthBar to .75
                    if (healthBar < (leftHealth - .025)): #Only update if health difference is larger than 2.5%
                        leftHealth = healthBar
                    break
    
            for x in range(x_RightHealthbarStart, x_RightHealthbarEnd, -1): #find first pixel of normal healthbar
                if gFrame[y_MidHealthbar][x] == 204:
                    healthBar = 1-((x_RightHealthbarStart-x)/(x_RightHealthbarStart-x_RightHealthbarEnd))# essentially if it was found 1/4 way through is would set healthBar to .75
                    if (healthBar < (rightHealth - .025)): #Only update if health difference is larger than 2.5%
                        rightHealth = healthBar
                    break
            return [leftHealth, rightHealth]