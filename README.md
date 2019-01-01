# Twitch Plays Click Bot
*"A bot that barely works and no one asked for."*

# Notes
+ Library Dependencies: pywin32, opencv2, scipy, numpy, selenium, gecko driver (place in bot folder)
+ Environment Dependencies: Windows 7+, Python 3.x, OBS, Abode Flash Projector, Two monitors (1 real + 1 simulated or 2 real)
+ This bot is a work in progress! Expect things to not work properly or at all. Expect frequent stream cutouts for hot fixing or scheduled downtime for new feature implementations.
+ This is just an experiment, and I don't expect interest for it to last long. I will probably only have it running for a few weeks.
+ I will make the source code to this bot open source after I implement all the features I want.
+ I do not care if spaces are better than tabs!
+ Windows API is absolutely the worst API I have ever worked with (not even counting this project)
+ Linux drivers for video recording/streaming glitch out!

# Change Log
## Version 0.2:
+ Converted bot to new environment for better performance
+ Working on game compatibility
## Version 0.1:
+ Basic features of bot complete: winning click detection and clicking locations
+ Simple tests conducted: performance while streaming very poor

# To Do:
+ Winning click not registering
+ Do real time test
+ Can you click on end game?
+ Message to leave click browser maximized in background
+ Make inputs also have date time
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

# How to Play:
+ Enable the Smart Click Map extension, located in the stream player controls.
+ Click on the stream window to vote where you want the next mouse click to be.
+ The click map overlay will update to show where the most votes are being made.
+ At the end of a voting round (typically 30 seconds), the bot will click at the geometric center of the winning location.
+ The voting will then be reset and you can vote again for the next spot.
+ There are no chat-based commands for this bot. Clicking on the stream is the only way to interact with the game.
+ It may take a few seconds for the click map overlay to register votes, especially if there aren't many votes being made.
+ If the click map doesn't display ANY locations during a round, not enough votes have been cast. Try clicking a spot several times to have it register.

# Game Integration Notes
Need to find more games that are compatible, mainly tower defense or strategy
Link escape: A web link embedded in the flash game that opens a browser
## Bloons Tower Defense 1, 2, 3:
+ 1 and 2 are bad, but would work with the bot very well
+ 3 seems to work fine without alterations;
+ No link escapes
## Canyon Defense:
+ Has timed rounds, which is bad for bot response time; Edited game for more time
+ No link escapes
## Bloons TD4 + Expansion and Bloons TD 5:
+ Have many link escapes
+ Game view not scale correctly
+ Need to remove all URL links
+ Alternative: find out how to block outbound requests from flash player (firewall?)
## Pandemic 2:
+ Requires click and drag to play; Not possible with this bot
## Desktop Tower Defense:
+ Has continuous timer for rounds; Could edit game to slow down or stop
+ Seems to be no link escapes
## Viking Defense:
+ Won't load in flash player