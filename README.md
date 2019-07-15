# Twitch Plays Click Bot
*"A bot that barely works and no one asked for."*

Using the [Smart Click Maps addon](https://twitch.exmachina.nl), [twitch.tv](https://twitch.tv) viewers can click to vote where a bot will click in-game. This uses OpenCV to interface between the click map and bot since there was no exisiting API to get exact click locations at the time.

# Notes
+ Library Dependencies: pywin32, pyautogui, opencv2, scipy, numpy, selenium, gecko driver (place binary in main folder)
+ Environment Dependencies: Windows 10, Python 3.x, OBS, Abode Flash Projector (v32), Firefox, Two monitors (1 real + 1 simulated or 2 real)
+ This bot is a work in progress! Expect things to not work properly or at all.
+ This is just an experiment, and I don't expect interest for it to last long.
+ I do not care if spaces are better than tabs! I use tabs in every other language, so I use tabs in Python!
+ Windows API is the worst API I have ever worked with (not even counting this project).
+ Linux drivers for video recording/streaming glitch out and make flashing artifacts appear on streams.
+ I already realize there are an infinite amount of better ways to create this bot.

# Change Log
## Version 0.2:
+ Converted bot to new environment for better performance
+ Working on game compatibility
+ Fixed process click location offset bug
+ Now only resets click map unless winning spot is found
+ Shows graphic where click occurred
## Version 0.1:
+ Basic features of bot complete: winning click detection and clicking locations
+ Simple tests conducted: performance while streaming very poor

# To Do:
+ Iterate version to 0.3
+ Reset click map after 2 no click rounds
+ Add countdown to stream display
+ Make inputs also have date time
+ Message to leave click browser maximized in background
+ Catch interrupt to auto close browser
+ Make sure popout is above task bar
+ Create github repo (WITHOUT THE SECRET URL!!!!)
+ Block internet access to flash player
+ Automatically open, load, and maximize Flash player
+ Exit option while sleeping
+ Pause option while sleeping
+ Send email in the event of a crash
+ Add event logging
+ Compress old click maps
