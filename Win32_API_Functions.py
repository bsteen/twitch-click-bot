import ctypes
from ctypes import wintypes		# WHY DO I NEED TO EXPLICITLY IMPORT WINTYPES FOR IT TO WORK?!?!?!
import datetime
import pyautogui
import win32api
import win32con
import win32gui
import time

# Gets the Windows handle for a window, a.k.a: "hwnd"
def get_window_handle(window_name):
	hwnd = win32gui.FindWindow(None, window_name)
	if hwnd == 0:
		return None
	else:
		return hwnd

# Move mouse to a location and left click
def click(x, y):
	win32api.SetCursorPos((x,y))
	time.sleep(0.1)		# Moving and clicking right away may be too fast for it to register?
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
	time.sleep(0.1)
	return

# Just move the mouse cursor
def move(x, y):
	win32api.SetCursorPos((x,y))
	return


# Use built-in Windows function to draw circle around mouse location
# Must be enabled in Windows settings: Mouse Properties > Pointer Options > "Show location of pointer when I press CTRL key"
# I couldn't get the CTRL key to be detected with win32api.keybd_event(...); it would send they key to a window's context, but Windows didn't detect it
def show_mouse_location():
	pyautogui.press("ctrl")
	return

# Sets the given window so it is always on top of normal windows
def set_always_on_top(window_name):
	hwnd = get_window_handle(window_name)
	if hwnd == None:
		print(datetime.datetime.now(), "Failed to find \"{}\" window when setting as always on top!".format(window_name))
		return False

	error = win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, -1, -1, -1, -1, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
	if error == 0:
		print(datetime.datetime.now(), "Could not set windows \"{}\" to always on top!".format(window_name))
		return False

	return True

# Given a window's name, return the coordinates of the top left corner
def get_window_location(window_name):
	hwnd = get_window_handle(window_name)	# Check if window exists
	if hwnd == None:
		print(datetime.datetime.now(), "Failed to find \"{}\" window when trying to get its coordinates!".format(window_name))
		return (-1, -1)

	# rect = win32gui.GetWindowRect(hwnd)     # CAN'T USE THIS!!!!
	# # See link for reason why; fixed code used below is also from this answer
	# # https://stackoverflow.com/questions/3192232/getwindowrect-too-small-on-windows-7
	# return (rect[0], rect[1])

	# Get true window coordinates, a.k.a. a stupid hack for a hack-job API
	try:
		getWinAttr = ctypes.windll.dwmapi.DwmGetWindowAttribute
	except WindowsError:
		print(datetime.datetime.now(), "Failed to get \"{}\" window coordinates!".format(window_name))
		return (-1, -1)

	win_rect = ctypes.wintypes.RECT()
	dwmwa_extended_frame_bounds = 9
	getWinAttr(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(dwmwa_extended_frame_bounds), ctypes.byref(win_rect), ctypes.sizeof(win_rect))
	x = win_rect.left
	y = win_rect.top

	# Make sure window is not minimized
	if x < 0 or y < 0:
		print(datetime.datetime.now(), "Window \"{}\" seems to be minimized. Un-minimize window!".format(window_name))
		return (1, -1)

	return (x, y)

# Given a window's name, return the , return the dimensions (width, height) of the window
def get_window_dim(window_name):
	hwnd = get_window_handle(window_name)
	if hwnd == None:
		print(datetime.datetime.now(), "Failed to find \"{}\" window when trying to get its dimensions!".format(window_name))
		return (-1, -1)

	try:
		getWinAttr = ctypes.windll.dwmapi.DwmGetWindowAttribute
	except WindowsError:
		print(datetime.datetime.now(), "Failed to get \"{}\" window dimensions!".format(window_name))
		return (-1, -1)

	win_rect = ctypes.wintypes.RECT()
	dwmwa_extended_frame_bounds = 9
	getWinAttr(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(dwmwa_extended_frame_bounds), ctypes.byref(win_rect), ctypes.sizeof(win_rect))
	width = win_rect.right - win_rect.left
	height =  win_rect.bottom - win_rect.top

	# Make sure window is not minimized
	if win_rect.left < 0 or win_rect.top < 0:
		print(datetime.datetime.now(), "Window \"{}\" seems to be minimized. Un-minimize window!".format(window_name))
		return (1, -1)

	return (width, height)