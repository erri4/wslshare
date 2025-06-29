import time
import pyautogui
import keyboard


def write(text: str):
    if len(text.split(r'\n')) == 1:
        keyboard.write(text)
        return
    for line in text.split(r'\n')[:-1]:
        keyboard.write(line)
        pyautogui.keyDown('shift')
        pyautogui.press('enter')
        pyautogui.keyUp('shift')
    keyboard.write(text.split(r'\n')[-1])
    

def open_whatsapp():
    pyautogui.press('win')
    keyboard.write('whatsapp')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)


def send_message(contact_name, message):
    open_whatsapp()
    pyautogui.hotkey('ctrl', 'f')
    for i in range(10):
        pyautogui.press('backspace')
    keyboard.write(contact_name) # pyautogui not working for non english languages
    pyautogui.press('enter')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('enter')
    while True:
        write(message)
        pyautogui.press('enter')


if __name__ == '__main__':
    contact_name = input('contact_name: ')
    message = input('message: ')
    send_message(contact_name, message)
