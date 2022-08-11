from contextlib import nullcontext
from ctypes import *
from ctypes.wintypes import *
import json

def get_active_window_name():
    try:
        user32 = windll.user32
        hwnd = user32.GetForegroundWindow()	
        pid = DWORD()
        user32.GetWindowThreadProcessId(hwnd, byref(pid))
        length = user32.GetWindowTextLengthW(hwnd)
        buff = create_unicode_buffer(256)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value
    except Exception as e:
        print(e)
        return ""

def set_cursor_pos(x, y):
    user32 = windll.user32
    user32.SetCursorPos(x, y)

def is_window_active(window_name):
    if get_active_window_name() == window_name:
        return True
    return False

def test():
    if get_active_window_name() == "FreePIE - Programmable Input Emulator":
        return True
    return False

def import_json(filename): 
    f = open(filename)
    data = json.load(f)
    f.close()
    return data

def reload_json_changes(json_content, filename): 
    f = open(filename)
    data = json.load(f)
    f.close()
    if data == json_content:
        return None
    else:
        return data
