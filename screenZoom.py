import cv2
import numpy as np
import pyautogui
import keyboard
import time

# Get screen size
screen_width, screen_height = pyautogui.size()

# Define window size (adjust as needed)
window_width, window_height = 100, 100

# Calculate center position
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

# Set initial region (directly behind the window)
region = (window_x, window_y, window_width, window_height)

# Create a named window and move it to the center
cv2.namedWindow("Screen Reflection", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Screen Reflection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("Screen Reflection", cv2.WND_PROP_TOPMOST, 1)  # Keep on top
cv2.setWindowProperty("Screen Reflection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
cv2.resizeWindow("Screen Reflection", window_width, window_height)
cv2.moveWindow("Screen Reflection", window_x, window_y)

while True:
    # Capture the area behind the window
    screen_width, screen_height = pyautogui.size()
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2
    region = (window_x, window_y, window_width, window_height)
    screenshot = pyautogui.screenshot(region=region)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Display the updated screen capture
    cv2.imshow("Screen Reflection", frame)

    # Exit on Ctrl + F9
    if keyboard.is_pressed("ctrl+f9"):
        break

    # Allow OpenCV to process key events
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
