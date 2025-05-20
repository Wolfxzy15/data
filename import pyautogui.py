import pyautogui
import time

print("Shift presser started. Press Ctrl+C to stop.")

try:
    while True:
        pyautogui.press('shift')
        print("Pressed Shift")
        time.sleep(90)
except KeyboardInterrupt:
    print("Stopped.")
