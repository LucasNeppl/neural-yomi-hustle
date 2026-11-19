import keyboard
import mss
import cv2
import numpy as np
import pyautogui
import time
import math

pyautogui.PAUSE = 0     #removes .1 delay between pyautogui actions


def running_loop():
    target_window = {"top": 0, "left": 0, "width": 1919, "height": 1079}
    #Format raw_frame[y][x][0]
    
    leftAttackButtons = np.array([(15, 879), (66, 879), (117, 879), (15, 930), (177, 879), (228, 879), (279, 879), (177, 930), (339, 879), (390, 879), (441, 879), (339, 930), (390, 930), (441, 930), (339, 981), (390, 981), (501, 879), (552, 879), (603, 879), (501, 930), (552, 930), (603, 930), (501, 981), (552, 981), (603, 981), (663, 879), (714, 879), (765, 879), (663, 930), (714, 930), (765, 930), (822, 876)])
    rightAttackButtons = np.array([(1749, 879), (1800, 879), (1851, 879), (1749, 930), (1587, 879), (1638, 879), (1689, 879), (1587, 930), (1425, 879), (1476, 879), (1527, 879), (1425, 930), (1476, 930), (1527, 930), (1425, 981), (1476, 981), (1263, 879), (1314, 879), (1365, 879), (1263, 930), (1314, 930), (1365, 930), (1263, 981), (1314, 981), (1365, 981), (1101, 879), (1152, 879), (1203, 879), (1101, 930), (1152, 930), (1203, 930), (966, 876)])

    time.sleep(4)
    with mss.MSS() as sct:
        while keyboard.is_pressed('q') == False: #run until q is pressed

            # click hold for both characters before grabbing screenshot
            #pyautogui.click(822, 876)
            #pyautogui.click(966, 876)
            #raw_frame = np.array(sct.grab(target_window)) #grab the screen. In format of R, G, B, A
            #gray_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
            # 
            #
            
            
            for i in range(len(leftAttackButtons)):
                if keyboard.is_pressed('q'): #Break loop if q pressed
                    break
                lx, ly = leftAttackButtons[i] #Grab coordinates from array
                pyautogui.click(lx, ly) #Click at coordinates
                for j in range(len(rightAttackButtons)):
                    rx, ry = rightAttackButtons[j]
                    print(f"Attack Button {i + 1}, {j + 1}: Left X={lx}, Y={ly}; Right X={rx}, Y={ry}")
                    pyautogui.click(rx, ry)
                    time.sleep(.125) # 1/8 second delay so this renders 8 attacks per second. This get almost all attacks rendered (>=97.5%) (but i think it's possible for some to be too slow still)
                    #when adding screenshot grabbing could make run faster on some attacks and guarantee all attacks render but either way when you have max or close to max it is slow like 1:30 to 2 minutes
                    # could try to improve game performance to get maybe 10 per second but again this is kinda minor 
                    # but those chnages and other could add up so idk but im really running into thwe fabled n^2 boggy man

            break #temp loop break

            # time.sleep(2) #Wait
            # coords = pyautogui.position()
            # x, y = coords
            # if (raw_frame[y][x][0] != 15):
            #     print("hovering over button")
            # else:
            #     print("not hovering over button")
            # time.sleep(1) #Wait
            # print (str(raw_frame[y][x][0]))




if __name__ == "__main__":
    running_loop()
