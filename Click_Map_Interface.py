from selenium import webdriver
import os
import time
import datetime
import base64
import Win32_API_Functions

class Click_Map_Control:
	def __init__(self, one_vote, click_map_popout_name):
		self.window_name = click_map_popout_name
		self.width = 322			# constant value
		self.height = 401			# constant value
		self.one_vote = one_vote 	# Is a single player allow to vote more than once per round? Set by main module

	# Try to set popout as always on top
	# Function will stall program and try again until it succeeds
	def set_popout_always_on_top(self):
		result = Win32_API_Functions.set_always_on_top(self.window_name)

		while result == False:
			print(datetime.datetime.now(), end= " ")
			input("Fix issue then press enter to continue...")
			result = Win32_API_Functions.set_always_on_top(self.window_name)
		print(datetime.datetime.now(), "Set \"{}\" to always on top".format(self.window_name))

		return

	# Find pop out's window location (top left corner of popout window)
	# Get the location of the popout everytime, in case it was moved in between rounds
	# Function will stall program and try again until it succeeds
	def get_popout_location(self):
		task_failed = False

		x, y = Win32_API_Functions.get_window_location(self.window_name)
		while x == -1 or y == -1:
			task_failed = True
			print(datetime.datetime.now(), end= " ")
			input("Fix issue then press enter to try again...")
			x, y = Win32_API_Functions.get_window_location(self.window_name)

		if task_failed:
			self.verify_popout_integrity()

		return (x, y)

	# Check if click map control window is open and the correct size
	# Function will stall program and try again until it succeeds
	def verify_popout_integrity(self):
		check_failed = False

		result = Win32_API_Functions.get_window_handle(self.window_name)
		while result == None:
			check_failed = True
			print(datetime.datetime.now(), end= " ")
			input("Could not find Smart Click popout window. Open popout and press enter...")
			result = Win32_API_Functions.get_window_handle(self.window_name)

		w, h = Win32_API_Functions.get_window_dim(self.window_name)
		while w != self.width or h != self.height:
			check_failed = True
			print(datetime.datetime.now(), end= " ")
			input("Don't minimize or change the size of the popout window! Reopen/un-minimize window and try again...")
			w, h = Win32_API_Functions.get_window_dim(self.window_name)

		if check_failed:
			self.set_popout_always_on_top()

		return

	# Should only need to be called once during the program
	# Goes from main menu to starting first round of clicking by clicking buttons in pop out controller
	def start_click_map(self):
		self.set_popout_always_on_top()
		self.verify_popout_integrity()		# Always verify integrity of popout before clicking
		x, y = self.get_popout_location()

		# Click buttons to start the Click map
		Win32_API_Functions.click(x + 164, y + 176)	# Select "Click Map"
		time.sleep(0.4)

		# Select check box to enable one vote per viewer
		if self.one_vote:
			Win32_API_Functions.click(x + 29, y + 115)
			time.sleep(0.4)

		Win32_API_Functions.click(x + 162, y + 334)	# Select "Start Click Map"

		return

	# Restarts the click map; Basically, it clears all votes for a new round to start
	# Called at either the start or end of a round
	def restart_click_map(self):
		self.verify_popout_integrity()
		x, y = self.get_popout_location()

		Win32_API_Functions.click(x + 161, y + 335)	# Select "Stop"
		time.sleep(0.4)								# Give enough time for click to register
		Win32_API_Functions.click(x + 241, y + 335)	# Select "Close"
		time.sleep(0.4)
		Win32_API_Functions.click(x + 235, y + 335)	# Select "Restart"

		return

	# End the click map; Voters can no longer click the screen
	def stop_click_map(self):
		self.verify_popout_integrity()
		x, y = self.get_popout_location()

		Win32_API_Functions.click(x + 161, y + 335)	# Select "Stop"
		time.sleep(0.4)
		Win32_API_Functions.click(x + 241, y + 335)	# Select "Close"
		time.sleep(0.4)
		Win32_API_Functions.click(x + 89, y + 335)	# Select "Main Menu"

		return

class Click_Map_Downloader:
	def __init__(self, URL):
		self.click_map_URL = URL

		cwd = os.getcwd()
		os.environ["PATH"] += os.pathsep + cwd  # Set location of geckodriver binary to the current running folder

		self.driver = webdriver.Firefox()    	# Start Firefox browser
		self.driver.maximize_window()			# Set size so click map scales correctly; fullscreen or not doesn't seem to matter
		self.driver.get(self.click_map_URL)		# Navigate to click map url

	# Reload browser page
	def reload_page(self):
		self.driver.get(self.click_map_URL)

	# Close the browser
	def close_browser(self):
		self.driver.close()

	# Gets click map image from browser, returns image data
	# https://stackoverflow.com/a/38318578
	def download_click_map(self):
		canvas = self.driver.find_element_by_css_selector("canvas")		# Find the canvas (image of click map)
		canvas_base64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)	# get the canvas as a PNG base64 string
		canvas_png = base64.b64decode(canvas_base64) 					# Decode base64 to image

		# save raw click map to a file
		# image_name = "click_maps/click_map_" + str(self.map_number) + ".png"
		# with open(image_name, 'wb') as img_file:
		# 	img_file.write(canvas_png)
		# self.map_number += 1

		return canvas_png