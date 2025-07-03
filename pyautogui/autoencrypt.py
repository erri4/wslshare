from encrypter import RotorEncryptor
from getkey import map_char
import string
import keyboard

def is_modifier(key_name: str):
    return key_name in {'ctrl', 'ctrl_l', 'ctrl_r', 'alt', 'alt_l', 'alt_r'}

def on_key(event: keyboard.KeyboardEvent):
    global modifiers_pressed

    if event.event_type == "down":
        if is_modifier(event.name):
            modifiers_pressed.add(event.name)
            return

        if modifiers_pressed:
            return

        if event.name == 'backspace':
            encryptor.rotates = max(encryptor.rotates - 1, 0)
            return

        if event.name is None or len(event.name) != 1:
            return

        char = event.name
        if char.isprintable():
            keyboard.send('backspace')
            encrypted = encryptor.rotate(char if map_char(char) == char.lower() else map_char(char))
            keyboard.write(encrypted)

    elif event.event_type == "up":
        if is_modifier(event.name):
            modifiers_pressed.discard(event.name)


if __name__ == '__main__':
    if input('encrypt or decrypt? (e/d)') == 'e':
        key = input('key: (in the form of "j: 1, 2, 1, 3 d: up, down, up")')
        wheels = [string.ascii_lowercase, string.ascii_uppercase, 'אבגדהוזחטיכלמנסעפצקרשת']
        if input('add wheels? (y/n)') == 'y':
            morewheel = input('wheel (type stop to stop)')
            while not morewheel == 'stop':
                wheels.append(morewheel)
        encryptor = RotorEncryptor(key, *wheels)

        modifiers_pressed = set()

        keyboard.hook(on_key)
        print('now encrypting everything you type! press escape to stop')
        keyboard.wait('esc')
    else:
        key = input('key: (in the form of "j: 1, 2, 1, 3 d: up, down, up")')
        wheels = [string.ascii_lowercase, string.ascii_uppercase, 'אבגדהוזחטיכלמנסעפצקרשת']
        if input('add wheels? (y/n)') == 'y':
            morewheel = input('wheel (type stop to stop)')
            while not morewheel == 'stop':
                wheels.append(morewheel)
        encryptor = RotorEncryptor(key, *wheels)
        text = list(input('text:'))
        for i in range(len(text)):
            text[i] = encryptor.rotate(text[i], -1)
        print(''.join(text))
