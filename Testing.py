import keyboard
import mss
import cv2
import numpy as np
import pyautogui
import time
import math

pyautogui.PAUSE = 0     #removes .1 delay between pyautogui actions


def running_loop():
    target_window = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    #Format raw_frame[y][x][0]
    
    list_of_left_attack_options = []
    list_of_left_attack_buttons_pos = []
    list_of_right_attack_options = []
    list_of_right_attack_buttons_pos = []

    #leftAttackButtons = np.array([(15, 879), (66, 879), (117, 879), (15, 930), (177, 879), (228, 879), (279, 879), (177, 930), (339, 879), (390, 879), (441, 879), (339, 930), (390, 930), (441, 930), (339, 981), (390, 981), (501, 879), (552, 879), (603, 879), (501, 930), (552, 930), (603, 930), (501, 981), (552, 981), (603, 981), (663, 879), (714, 879), (765, 879), (663, 930), (714, 930), (765, 930), (822, 876)])
    #rightAttackButtons = np.array([(1749, 879), (1800, 879), (1851, 879), (1749, 930), (1587, 879), (1638, 879), (1689, 879), (1587, 930), (1425, 879), (1476, 879), (1527, 879), (1425, 930), (1476, 930), (1527, 930), (1425, 981), (1476, 981), (1263, 879), (1314, 879), (1365, 879), (1263, 930), (1314, 930), (1365, 930), (1263, 981), (1314, 981), (1365, 981), (1101, 879), (1152, 879), (1203, 879), (1101, 930), (1152, 930), (1203, 930), (966, 876)])

    time.sleep(4)
    with mss.MSS() as sct:
        while keyboard.is_pressed('q') == False: #run until q is pressed

            # click hold for both characters before grabbing screenshot
            #pyautogui.click(822, 876)
            #pyautogui.click(966, 876)


            
            raw_frame = np.array(sct.grab(target_window)) #grab the screen. In format of R, G, B, A
            gray_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY) # converts to gray scale single value

            

            lockInLeft = [-1, -1]
            lockInRight = [-1, -1]
            findButtons("left", list_of_left_attack_options, list_of_left_attack_buttons_pos, lockInLeft, target_window, gray_frame)
            findButtons("right", list_of_right_attack_options, list_of_right_attack_buttons_pos, lockInRight, target_window, gray_frame)

            leftAttackOptions = np.array(list_of_left_attack_options)
            leftAttackButtonsPos = np.array(list_of_left_attack_buttons_pos)
            rightAttackOptions = np.array(list_of_right_attack_options)
            rightAttackButtonsPos = np.array(list_of_right_attack_buttons_pos)

            list_of_left_attack_options.clear()
            list_of_left_attack_buttons_pos.clear()
            list_of_right_attack_options.clear()
            list_of_right_attack_buttons_pos.clear()
            

            #main attack loop
            m = 1
            for i in range(len(leftAttackButtonsPos)):
                if keyboard.is_pressed('q'): #Break loop if q pressed
                    break
                lx = leftAttackButtonsPos[i][0] #Grab coordinates from array
                ly  = leftAttackButtonsPos[i][1]
                pyautogui.click(lx, ly) #Click at coordinates
                for j in range(len(rightAttackButtonsPos)):
                    if keyboard.is_pressed('q'): #Break loop if q pressed
                        break
                    rx = rightAttackButtonsPos[j][0] #Grab coordinates from array
                    ry  = rightAttackButtonsPos[j][1]
                    print(f"Attack Button {i + 1}, {j + 1}: Left X={lx}, Y={ly}; Right X={rx}, Y={ry}")
                    pyautogui.click(rx, ry)
                    
                    time.sleep(.125) 
                    # 1/8 second delay so this renders 8 attacks per second. This get almost all attacks rendered (>=97.5%) (but i think it's possible for some to be too slow still)
                    #when adding screenshot grabbing could make run faster on some attacks and guarantee all attacks render but either way when you have max or close to max it is slow like 1:30 to 2 minutes
                    # could try to improve game performance to get maybe 10 per second but again this is kinda minor 
                    # but those chnages and other could add up so idk but im really running into thwe fabled n^2 boggy man
            
            time.sleep(4) 



# def testing_screenshot():
#     target_window = {"top": 0, "left": 0, "width": 1920, "height": 1080}
#     #Format raw_frame[y][x][0]
    
#     # gray scale shap is (1080, 1920)
#     # background is 12

#     time.sleep(5)
#     with mss.MSS() as sct:
#         raw_frame = np.array(sct.grab(target_window)) #grab the screen. In format of R, G, B, A
#         gray_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY) # converts to gray scale single value
#         cv2.imshow('GrayFrame: ', gray_frame)
#         while keyboard.is_pressed('q') == False: #run until q is pressed
            
#             # click hold for both characters before grabbing screenshot
#             #pyautogui.click(822, 876)
#             #pyautogui.click(966, 876)
#             #raw_frame = np.array(sct.grab(target_window)) #grab the screen. In format of R, G, B, A
#             #gray_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
#             # 
#             #

            

#             if cv2.waitKey(25) & 0xFF == ord("q"):
#                 cv2.destroyAllWindows()
#                 break

            

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




if __name__ == "__main__":
    
    
    running_loop()
    #testing_screenshot()
