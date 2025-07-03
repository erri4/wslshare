import ctypes
from ctypes import wintypes


user32 = ctypes.WinDLL("user32", use_last_error=True)

GetKeyboardLayout = user32.GetKeyboardLayout
GetKeyboardLayout.restype = wintypes.HKL
GetKeyboardLayout.argtypes = [wintypes.DWORD]

MapVirtualKey = user32.MapVirtualKeyW
MapVirtualKey.restype = wintypes.UINT
MapVirtualKey.argtypes = [wintypes.UINT, wintypes.UINT]

ToUnicodeEx = user32.ToUnicodeEx
ToUnicodeEx.restype = ctypes.c_int
ToUnicodeEx.argtypes = [
    wintypes.UINT,                 # virtual-key code
    wintypes.UINT,                 # scan code
    ctypes.POINTER(ctypes.c_ubyte),  # key state array
    ctypes.c_wchar_p,              # output buffer
    ctypes.c_int,                  # buffer size
    wintypes.UINT,                 # flags
    wintypes.HKL                   # keyboard layout
]

GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = wintypes.HWND

GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
GetWindowThreadProcessId.restype = wintypes.DWORD

def get_active_keyboard_layout():
    hwnd = GetForegroundWindow()
    thread_id = GetWindowThreadProcessId(hwnd, None)
    return GetKeyboardLayout(thread_id)

def map_char(char: str) -> str:
    if not (char.isalpha() and len(char) == 1):
        raise ValueError("Input must be a single alphabetic character (a-z or A-Z).")

    vk_code = ord(char.upper())
    scan_code = MapVirtualKey(vk_code, 0)
    layout = get_active_keyboard_layout()

    key_state = (ctypes.c_ubyte * 256)()
    output_buffer = ctypes.create_unicode_buffer(8)

    result = ToUnicodeEx(vk_code, scan_code, key_state, output_buffer, len(output_buffer), 0, layout)

    return output_buffer.value or char