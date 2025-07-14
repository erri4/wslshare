import tkinter as tk
from tkinter import simpledialog, messagebox
from encrypter import RotorEncryptor
from getkey import map_char
import string
import keyboard
import threading

class RotorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Rotor Mini")
        self.root.geometry("227x265")
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", True)

        self.mode = tk.StringVar(value="decrypt")
        self.wheels = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            "אבגדהוזחטיכלמנסעפצקרשת"
        ]
        self.encryptor = None
        self.modifiers_pressed = set()
        self.hooking = False

        font_opts = ("Arial", 8)

        self.toggle_btn = tk.Button(root, text="Mode: Decrypt", command=self.toggle_mode, font=font_opts)
        self.toggle_btn.pack(pady=2)

        tk.Label(root, text="Key in the form of 'j: 1, 3, 2 d: up, down' :", font=font_opts).pack()
        self.key_entry = tk.Entry(root, font=font_opts)
        self.key_entry.pack()

        tk.Button(root, text="Add Wheel", command=self.add_wheel, font=font_opts).pack(pady=2)

        self.text_label = tk.Label(root, text="Text:", font=font_opts)
        self.text_label.pack()
        self.text_entry = tk.Entry(root, font=font_opts)
        self.text_entry.pack()

        self.run_button = tk.Button(root, text="Run", command=self.run, font=font_opts)
        self.run_button.pack(pady=2)

        self.output_label = tk.Label(root, text="", wraplength=210, font=font_opts)
        self.output_label.pack()

        self.stop_button = tk.Button(root, text="Start Encryption", command=self.toggle_encryption, font=font_opts)
        self.stop_button.pack(pady=2)

        self.update_visibility()

    def toggle_mode(self):
        if self.mode.get() == "decrypt":
            self.mode.set("encrypt")
            self.toggle_btn.config(text="Mode: Encrypt")
        else:
            self.mode.set("decrypt")
            self.toggle_btn.config(text="Mode: Decrypt")
        self.update_visibility()

    def update_visibility(self):
        is_encrypt = self.mode.get() == "encrypt"
        for widget in [self.text_label, self.text_entry, self.run_button, self.output_label]:
            widget.pack_forget() if is_encrypt else widget.pack()
        if is_encrypt:
            self.stop_button.config(text="Stop Encryption" if self.hooking else "Start Encryption")
            self.stop_button.pack(pady=2)
        else:
            self.stop_button.pack_forget()

    def add_wheel(self):
        wheel = simpledialog.askstring("Add Wheel", "Enter custom wheel:")
        if wheel:
            self.wheels.append(wheel.strip())

    def run(self):
        key = self.key_entry.get()
        if not key:
            messagebox.showwarning("Missing Key", "Please enter a key.")
            return

        try:
            self.encryptor = RotorEncryptor(key, *self.wheels)
        except Exception as e:
            messagebox.showerror("Key Error", str(e))
            return

        if self.mode.get() == "decrypt":
            text = self.text_entry.get()
            result = [self.encryptor.rotate(ch, -1) for ch in text]
            self.output_label.config(text="".join(result))

    def toggle_encryption(self):
        key = self.key_entry.get()
        if not key:
            messagebox.showwarning("Missing Key", "Please enter a key.")
            return

        if not self.encryptor:
            try:
                self.encryptor = RotorEncryptor(key, *self.wheels)
            except Exception as e:
                messagebox.showerror("Key Error", str(e))
                return

        if not self.hooking:
            self.hooking = True
            threading.Thread(target=self.start_encryption_hook, daemon=True).start()
            self.update_visibility()
        else:
            self.stop_encryption()

    def start_encryption_hook(self):
        keyboard.hook(self.on_key)
        keyboard.wait('esc')
        self.stop_encryption()

    def stop_encryption(self):
        if self.hooking:
            self.encryptor.rotates = 0
            keyboard.unhook_all()
            self.hooking = False
            self.update_visibility()

    def is_modifier(self, key_name):
        return key_name in {'ctrl', 'ctrl_l', 'ctrl_r', 'alt', 'alt_l', 'alt_r'}

    def on_key(self, event: keyboard.KeyboardEvent):
        if event.event_type == "down":
            if self.is_modifier(event.name):
                self.modifiers_pressed.add(event.name)
                return

            if self.modifiers_pressed:
                return

            if event.name == 'backspace':
                self.encryptor.rotates = max(self.encryptor.rotates - 1, 0)
                return

            if event.name is None or len(event.name) != 1:
                return

            char = event.name
            if char.isprintable():
                keyboard.send('backspace')
                mapped = map_char(char)
                encrypted = self.encryptor.rotate(char if mapped == char.lower() else mapped)
                keyboard.write(encrypted)

        elif event.event_type == "up":
            if self.is_modifier(event.name):
                self.modifiers_pressed.discard(event.name)

if __name__ == "__main__":
    root = tk.Tk()
    app = RotorApp(root)
    root.mainloop()
