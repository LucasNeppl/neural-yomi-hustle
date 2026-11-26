import keyboard
from mss import MSS
import cv2
import numpy as np
import pyautogui
import time
import math

from compvision import ComputerVision
from capturewin import WindowCapture

class PlayerController:
    def __init__(self, target_Window, vision, capture, player):
        self.player = player
        self.capture = capture
        self.vision = vision
        self.window = target_Window
        self.scale_x = target_Window["width"] / 1920 #For example if window is 960x540 then scale_x = 0.5 and scale_y = 0.5
        self.scale_y = target_Window["height"] / 1080

        self.leftPlayerState = [1]
        self.rightPlayerState = [1]



    def getHealth(self, gFrame): #returns [leftHealth, rightHealth]
        return self.vision.getHealth(gFrame, self.leftPlayerState[0], self.rightPlayerState[0])
