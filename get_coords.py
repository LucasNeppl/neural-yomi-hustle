import pyautogui
import time

print("TOP-LEFT")
time.sleep(5)
left, top = pyautogui.position()
print(f"Recorded Top-Left: X={left}, Y={top}")

print("\nBOTTOM-RIGHT")
time.sleep(5)
right, bottom = pyautogui.position()

width = right - left
height = bottom - top

print(f"Recorded Bottom-Right: X={right}, Y={bottom}")
print(f'target_window = {{"top": {top}, "left": {left}, "width": {width}, "height": {height}}}')

i = 0
while i < 10:
    time.sleep(5)
    left, top = pyautogui.position()
    print(f"Recorded Position {i + 1}: X={left}, Y={top}")
    i += 1
            
