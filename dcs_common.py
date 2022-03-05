from ctypes import *
from ctypes.wintypes import *

user32 = windll.user32
window_name = "Digital Combat Simulator"

def get_active_window_name():
	
	hwnd = user32.GetForegroundWindow()	
	pid = DWORD()
	user32.GetWindowThreadProcessId(hwnd, byref(pid))
	try:
		length = user32.GetWindowTextLengthW(hwnd)
		buff = create_unicode_buffer(256)
		user32.GetWindowTextW(hwnd, buff, length + 1)
		return buff.value
	except Exception as e:
		return e

def is_dcs_active():
	if get_active_window_name() == window_name:
		return True
	return False

def test():
	if get_active_window_name() == "FreePIE - Programmable Input Emulator":
		return True
	return False

'''OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

PROCESS_ALL_ACCESS = 0x1F0FFF

address = 0x1000000  # Likewise; for illustration I'll get the .exe header.

if test():
	buffer = c_char_p("The data goes here")
	bufferSize = len(buffer.value)
	bytesRead = c_ulong(0)

	processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
if ReadProcessMemory(processHandle, address, buffer, bufferSize, byref(bytesRead)):
    print "Success:", buffer
else:
    print "Failed."

CloseHandle(processHandle)'''