import time
import pyautogui
import pygetwindow
import keyboard
import subprocess


def open_whatsapp():
    whatsapp_path = r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2445.7.0_x64__cv1g1gvanyjgm\WhatsApp.exe" # if you want to use this program replacethis with your whatsapp location
    # for getting your actual whatsapp location run dir "WhatsApp.exe" /S on C:\ in administrator commandline
    subprocess.Popen([whatsapp_path])
    time.sleep(5)


def focus_whatsapp_app():
    try:
        whatsapp_window = pygetwindow.getWindowsWithTitle("WhatsApp")[0]
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
