import time
import pyautogui
import pygetwindow
import keyboard
import subprocess


def open_whatsapp():
    pyautogui.press('win')
    time.sleep(1)
    keyboard.write('whatsapp')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)


def focus_whatsapp_app():
    try:
        whatsapp_window: pygetwindow.Win32Window = pygetwindow.getWindowsWithTitle("WhatsApp")[0]
        whatsapp_window.activate()
        time.sleep(1)
    except IndexError:
        print("WhatsApp window not found.")
        return False
    return True


def send_message(contact_name, message):
    if not focus_whatsapp_app():
        open_whatsapp()
        time.sleep(5)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    for i in range(10):
        pyautogui.press('backspace')
        time.sleep(1)
    keyboard.write(contact_name) # pyautogui not working for non english languages
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    while True:
        time.sleep(1)
        keyboard.write(message)
        pyautogui.press('enter')


if __name__ == '__main__':
    contact_name = input('contact_name: ')
    message = input('message: ')
    send_message(contact_name, message)
