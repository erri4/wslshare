from tkinter import messagebox as msgbox
import tkinter as tk
import asyncio

root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)


async def awaiter():
    await asyncio.sleep(0)


async def main():
    while True:
        print('hi')
        await awaiter()


async def win():
    while True:
        msgbox.showinfo("im innocent", 'msg')
        await awaiter()


async def start():
    await asyncio.gather(main(), win())


if __name__ == '__main__':
    asyncio.run(start())
