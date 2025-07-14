import tkinter as tk
import pytesseract
import threading
import time
import numpy as np
from PIL import ImageGrab
import pyautogui
import cv2

TARGET_WORD = "reef"
FRAME_DELAY = 1 / 600  # ~60 FPS

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)

TRANSPARENT_COLOR = 'magenta'
root.config(bg=TRANSPARENT_COLOR)
root.wm_attributes('-transparentcolor', TRANSPARENT_COLOR)

canvas = tk.Canvas(root, bg=TRANSPARENT_COLOR, highlightthickness=0)
canvas.pack(fill='both', expand=True)

boxes = []

def clear_boxes():
    for box in boxes:
        canvas.delete(box)
    boxes.clear()

def scan_and_overlay():
    screen_width, screen_height = pyautogui.size()

    while True:
        start_time = time.time()

        screenshot = ImageGrab.grab()
        img_width, img_height = screenshot.size

        img = np.array(screenshot)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        scale_x = screen_width / img_width
        scale_y = screen_height / img_height

        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

        clear_boxes()

        for i, word in enumerate(data['text']):
            if TARGET_WORD.lower() in word.strip().lower():
                x = int(data['left'][i] * scale_x)
                y = int(data['top'][i] * scale_y)
                w = int(data['width'][i] * scale_x)
                h = int(data['height'][i] * scale_y)

                rect = canvas.create_rectangle(x, y, x + w, y + h, fill='black', outline='')
                boxes.append(rect)

        elapsed = time.time() - start_time
        sleep_time = max(0, FRAME_DELAY - elapsed)
        time.sleep(sleep_time)

def exit_app(event):
    root.destroy()

threading.Thread(target=scan_and_overlay, daemon=True).start()

root.bind('<Escape>', exit_app)
root.mainloop()
