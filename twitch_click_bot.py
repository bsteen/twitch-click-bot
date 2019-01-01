import Detect_Click_Location
import Click_Map_Interface
import Win32_API_Functions
import time
import datetime
import sys

# Twitch Click Bot: Configured for Bloons TD3
# Uses Smart Click Map Plugin from Twitch

PROGRAM_VERSION = "0.2"			# Version number of the Twitch Click Bot
ROUND_TIME = 30 				# Length of a voting round in seconds; does not count time to process voting, only used to determine when voting should stop
ONE_VOTE_PER_VIEWER = False		# Is a single player allow to vote more than once per round?
FLASH_PLAYER_WINDOW = "Adobe Flash Player 32"
CLICK_MAP_POPOUT = "Smart Click Maps - Twitch - Mozilla Firefox"
GAME_WINDOW_X = 0
GAME_WINDOW_Y = 0

# Sets the global variables for the Flash player location
def record_game_window_location():
	global GAME_WINDOW_X
	global GAME_WINDOW_Y

	while(1):
		x, y = Win32_API_Functions.get_window_location(FLASH_PLAYER_WINDOW)
		if x == -1 or y == -1:
			input("Fix issue then press enter to try again...")
		else:
			break

	GAME_WINDOW_X = x
	GAME_WINDOW_Y = y
	print(datetime.datetime.now(), "Recorded \"{}\" window location at: {}, {}".format(FLASH_PLAYER_WINDOW, GAME_WINDOW_X, GAME_WINDOW_Y))

	return

# Verifies game is open first
# Sanitize out of bounds or dead zone coordinates, then click the area of the game
def process_click_request(x, y):
	# Check if game is still open
	check_if_game_open()

	# Keep clicks inside the playfield
	if x < 250 + GAME_WINDOW_X:		# Clicks too far left
		x = 250 + GAME_WINDOW_X
	elif x > 1670 + GAME_WINDOW_X:	# Clicks to far right
		x = 1670 + GAME_WINDOW_X

	if y < 10 + GAME_WINDOW_Y: 		# Clicked too high up
		y = 10 + GAME_WINDOW_Y
	elif y > 1060 + GAME_WINDOW_Y:	# Clicked too far down
		y = 1060 + GAME_WINDOW_Y

	Win32_API_Functions.click(x, y)	# Click at sanitized location
	print(datetime.datetime.now(), "Clicked at:", x, ",", y)

	return

# Check to see if flash player is still running
# Halts program if game is not found
def	check_if_game_open():
	hwnd = Win32_API_Functions.get_window_handle(FLASH_PLAYER_WINDOW)
	if hwnd == None:
		print(datetime.datetime.now(), "Could not find \"{}\" window!!!".format(FLASH_PLAYER_WINDOW))
		input("Reopen game window, make fullscreen on same screen as before, then press enter...")
		record_game_window_location()
		check_if_game_open()
	return

if __name__== "__main__":
	round_number = 1
	print(datetime.datetime.now(), "STARTING TWITCH CLICK BOT", PROGRAM_VERSION)

	print(datetime.datetime.now(), "Loading click map URL")
	file = open("click_map_url.txt", "r")
	click_map_URL =	file.readline().strip()
	file.close()

	print(datetime.datetime.now(), "Starting the click map browser")
	click_map_dl = Click_Map_Interface.Click_Map_Downloader(click_map_URL)	# Open up the click map

	input("Open the game player, make it full screen, then press enter...")
	print(datetime.datetime.now(), "Initial check of game window")
	check_if_game_open()
	record_game_window_location()
	result = Win32_API_Functions.set_always_on_top(FLASH_PLAYER_WINDOW) # Doesn't really matter if this fails; game window will be fullscreen anyway

	input("Open the popout click map controller in Firefox, then press enter...")
	print(datetime.datetime.now(), "Creating click map controller")
	click_map_ctrl = Click_Map_Interface.Click_Map_Control(ONE_VOTE_PER_VIEWER, CLICK_MAP_POPOUT)	# Create click map controller interface

	print(datetime.datetime.now(), "Creating click location detector")
	find_click_loc = Detect_Click_Location.Detect_Click_Location()

	input("READY! Press enter to start accepting votes...")
	print(datetime.datetime.now(), "Starting click map for the first time")
	click_map_ctrl.start_click_map()
	time.sleep(0.3)

	while(1):
		round_msg = "Round " + str(round_number) + " ends in:"
		print(datetime.datetime.now(), round_msg, end=" ")
		for i in range(ROUND_TIME, 0, -1):	# Print countdown to end of round in console
			print(i, end=" ")
			sys.stdout.flush()
			time.sleep(1)					# Sleep while the players vote
		print()
		sys.stdout.flush()

		image_png_data = click_map_dl.download_click_map()    				# Get image from click map URL
		x, y = find_click_loc.process_click_map(image_png_data, True)		# Proccess the click map; find winning click; log image
		if x != -1 or y != -1:
			print(datetime.datetime.now(), "Found winning click at: {}, {}".format(x, y))
			process_click_request(x, y)
		else:
			print(datetime.datetime.now(), "No winning click found!")

		round_number += 1
		click_map_ctrl.restart_click_map()

	click_map_ctrl.stop_click_map()
	click_map_dl.close_browser()
	print(datetime.datetime.now(), "***PROGRAM DONE; make sure to close all spawned windows and STOP STREAM***")