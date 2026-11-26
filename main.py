import keyboard
from mss import MSS
import cv2
import numpy as np
import pyautogui
import time
import math

from controller import PlayerController
from compvision import ComputerVision
from capturewin import WindowCapture

pyautogui.PAUSE = 0     #removes .1 delay between pyautogui actions

global leftPlayerState 
global rightPlayerState
global yomiTXT_NUM
global yomiTXT_f

def running_loop():
    target_Window = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    capture = WindowCapture(target_Window)
    vision = ComputerVision(target_Window, capture)
    control = PlayerController(target_Window, vision, capture, "left")

    list_of_left_attack_options = []
    list_of_left_attack_buttons_pos = []
    list_of_right_attack_options = []
    list_of_right_attack_buttons_pos = []

    #leftAttackButtons = np.array([(15, 879), (66, 879), (117, 879), (15, 930), (177, 879), (228, 879), (279, 879), (177, 930), (339, 879), (390, 879), (441, 879), (339, 930), (390, 930), (441, 930), (339, 981), (390, 981), (501, 879), (552, 879), (603, 879), (501, 930), (552, 930), (603, 930), (501, 981), (552, 981), (603, 981), (663, 879), (714, 879), (765, 879), (663, 930), (714, 930), (765, 930), (822, 876)])
    #rightAttackButtons = np.array([(1749, 879), (1800, 879), (1851, 879), (1749, 930), (1587, 879), (1638, 879), (1689, 879), (1587, 930), (1425, 879), (1476, 879), (1527, 879), (1425, 930), (1476, 930), (1527, 930), (1425, 981), (1476, 981), (1263, 879), (1314, 879), (1365, 879), (1263, 930), (1314, 930), (1365, 930), (1263, 981), (1314, 981), (1365, 981), (1101, 879), (1152, 879), (1203, 879), (1101, 930), (1152, 930), (1203, 930), (966, 876)])

    leftPlayerState = [1]
    rightPlayerState = [1]
    sct = MSS()

    time.sleep(4)

    while keyboard.is_pressed('q') == False: #run until q is pressed

        # click hold for both characters and without a delay screenshot to get player states before grabbing screenshot
        #pyautogui.click(822, 876)
        #pyautogui.click(966, 876)

        
        currentPlayer = "left"
        lockInLeft = [-1, -1]
        lockInRight = [-1, -1]
        findButtons("left", list_of_left_attack_options, list_of_left_attack_buttons_pos, lockInLeft, target_Window, gray_frame)
        findButtons("right", list_of_right_attack_options, list_of_right_attack_buttons_pos, lockInRight, target_Window, gray_frame)


        leftAttackOptions = np.array(list_of_left_attack_options)
        leftAttackButtonsPos = np.array(list_of_left_attack_buttons_pos)
        rightAttackOptions = np.array(list_of_right_attack_options)
        rightAttackButtonsPos = np.array(list_of_right_attack_buttons_pos)

        list_of_left_attack_options.clear()
        list_of_left_attack_buttons_pos.clear()
        list_of_right_attack_options.clear()
        list_of_right_attack_buttons_pos.clear()
        
        #main attack loop
        findPlayersState(leftAttackButtonsPos, rightAttackButtonsPos, target_Window, target_Window_Scale)
        scoreArray = gatherAttackScores(leftAttackButtonsPos, rightAttackButtonsPos, target_Window, target_Window_Scale)




        time.sleep(4) 



def gatherAttackScores(LAttackPos, RAttackPos, target_W, t_Window_Scale):
    m = 0
    attackScore = []
    for i in range(len(LAttackPos)):
        if keyboard.is_pressed('q'): #Break loop if q pressed
            break
        lx, ly = LAttackPos[i] #Grab coordinates from array
        pyautogui.click(lx, ly) #Click at coordinates
        for j in range(len(RAttackPos)):
            if keyboard.is_pressed('q'): #Break loop if q pressed
                break
            rx, ry = RAttackPos[j] #Grab coordinates from array
            print(f"Attack Button {i + 1}, {j + 1}: Left X={lx}, Y={ly}; Right X={rx}, Y={ry}")
            pyautogui.click(rx, ry)
            
            time.sleep(.2) #normally set to .125 temporarily set higher for testing to ensure rendered frames

            attackScore[m] = getScoreOfAttack(target_W, t_Window_Scale)
            # 1/8 second delay so this renders 8 attacks per second. This get almost all attacks rendered (>=97.5%) (but i think it's possible for some to be too slow still)
            #when adding screenshot grabbing could make run faster on some attacks and guarantee all attacks render but either way when you have max or close to max it is slow like 1:30 to 2 minutes
            # could try to improve game performance to get maybe 10 per second but again this is kinda minor 
            # but those chnages and other could add up so idk but im really running into thwe fabled n^2 boggy man
    



    return attackScore  
            

# #any missing set to zero (common for *_damage or *_hit since ussually only one character will land attack)
# moveDataFormat = [ #format follows top to bottom left to right when looking at screenshot
#     0, #0 left_damage (as in damage left player took)
#     200, #1 right_damage
#     13, #2 left_ready
#     40, #3 right_ready
#     7, #4 left_hit
#     0, #5 right_hit
#     200, #6 X_dif (Always Posistive X distance between both players predictions)
#     80, #7 Y_dif (Always Posistive Y distance between both players predictions)
# ] #add off some way to indicate off the ground potentially as that can be disadvantaguoes 
def getScoreOfAttack(t_W, t_W_Scale):
    attackData = np.zeros[8] #Array of move data

    raw_frame = np.array(sct.grab(t_W))
    gray_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)

    #damage is found by looking at healthbar 
    healthState = getHealth(t_W, t_W_Scale)
    attackData[0] = leftPlayerState[0] - healthState[0]
    attackData[1] = rightPlayerState[0] - healthState[1]

    #ready and hit frame found via template matching text (passes in grayframe cropped to the area we want)
    cropped_g_frame = gray_frame[270:291, 825:920]
    attackData[2] = getTextOneWindow(cropped_g_frame) # left ready
    cropped_g_frame = gray_frame[270:291, 1197:1250]
    attackData[3] = getTextOneWindow(cropped_g_frame) # right ready
    cropped_g_frame = gray_frame[300:321, 825:920]
    attackData[4] = getTextOneWindow(cropped_g_frame) # left hit
    cropped_g_frame = gray_frame[300:321, 1197:1250]
    attackData[5] = getTextOneWindow(cropped_g_frame) # right hit

    

    return attackData

def getPos():

    #masked image should be all black or white pixels
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)

#logic could be harder and slow down for trying to do custom scale so start with just one window logic
def getTextOneWindow(target):
    #First scane for 'f' to where digits are located
    result = 0
    threshold = 0.15
    res = cv2.matchTemplate(target, yomiTXT_f, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if (min_val > threshold):
        return 0 #if no match return 0 
    top_left_x = min_loc[0] 
    w, h = target.shape[::-1]
    crop_Digit1 = target[0:h, top_left_x-36:top_left_x-22] #Leave Y untouched and crop the 14 pixels wide number 
    crop_Digit2 = target[0:h, top_left_x-18:top_left_x-4] #Leave Y untouched and crop the 14 pixels wide number 
    res1 = cv2.matchTemplate(yomiTXT_NUM, crop_Digit1, cv2.TM_SQDIFF) # Note here the template is our cropped image
    res2 = cv2.matchTemplate(yomiTXT_NUM, crop_Digit2, cv2.TM_SQDIFF) # Note here the template is our cropped image
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
    if (min_val1 < threshold):
        top_left_x = min_loc1[0]
        result += 10 * (top_left_x // 18) # converts from array posistion to number then 10* since it's ten's digit
    top_left_x = min_loc2[0]
    result += (top_left_x // 18)
    return result


    


def findButtons(side, attackOptions, attackButtonsPos, lock_In, window, gray_frame):
    scale_x = window["width"] / 1920 #For example if window is 960x540 then scale_x = 0.5 and scale_y = 0.5
    scale_y = window["height"] / 1080
    padding = 24 * scale_x # how many pixels away from corner to click 24 is middle for default 48x48 buttons also important as pixel differences can add up but only to a small amount
    distBtwnBtns = 51 * scale_x # how many pixels between buttons 
    
    if side == "left":
        start_x = window["left"] + 16 * scale_x
        nextGroupXDist = 162 * scale_x
    elif side == "right":
        start_x = window["left"] + window["width"] - (20 + 150) * scale_x #right side are 20 pixels away not 16 and the 150 is get to the 1st button
        nextGroupXDist  = -162 * scale_x
    start_y = window["top"] + 879 * scale_y

    currentgroupx = start_x

    m = 0;
    for i in range(5):# 5 groups
        for j in range(9): # 9 buttons in each group
            x = math.ceil(currentgroupx + (j % 3) * distBtwnBtns + padding) # Modulus gives 0 1 2 0 1 ...
            y = math.ceil(start_y + (j // 3) * distBtwnBtns + padding) #floor division gives 0 0 0 1 1 1 2 ...
            if gray_frame[y][x] != 12: # if not background color then it is a button
                attackButtonsPos.append([x,y]) # save the button position
                m += 1
            else:
                break

        attackOptions.append(m)# save amount of buttons in each group
        m = 0
        currentgroupx += nextGroupXDist #move to the next group of buttons

    #finally add hold button option
    x = math.ceil(currentgroupx + padding)
    y = math.ceil(start_y + padding)
    attackButtonsPos.append([x,y])
    attackOptions.append(1)

    # Set lock in button
    y = math.ceil(y - distBtwnBtns)
    lock_In[0] = x;
    lock_In[1] = y;

# exPlayerState = [
#     .89 #playerHealth
    
# ]
def findPlayersState(LAttackPos, RAttackPos, t_Window, t_Window_Scale):
    lx, ly = LAttackPos[len(LAttackPos)-1] #Grab coordinates from array
    rx, ry = RAttackPos[len(RAttackPos)-1] #Grab coordinates from array
    pyautogui.click(lx, ly) #Click at coordinates
    pyautogui.click(rx, ry) #Click at coordinates
    time.sleep(.02)#Very short pause
    raw_frame = np.array(sct.grab(t_Window))
    gray_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
    healthState = getHealth(t_Window, t_Window_Scale, gray_frame)
    leftPlayerState[0] = healthState[0]
    rightPlayerState[0] = healthState[1]


if __name__ == "__main__":
    
    running_loop()
    # testing_screenshot()
