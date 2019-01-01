import cv2
import imutils
from scipy.spatial import distance
from collections import OrderedDict
import numpy as np
import datetime

# Code from: https://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/
class Detect_Click_Location:
	def __init__(self):
		self.map_number = 1 	# Number of maps processed; Should correspond with round number

		# initialize the colors dictionary, containing the color
		# name as the key and the RGB tuple as the value
		colors = OrderedDict({
			"winner": (0, 150, 135),		# Green
			"loser": (125, 85, 205)			# Purple
		})

		# allocate memory for the L*a*b* image, then initialize
		# the color names list
		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.colorNames = []

		# loop over the colors dictionary
		for (i, (name, rgb)) in enumerate(colors.items()):
			# update the L*a*b* array and the color names list
			self.lab[i] = rgb
			self.colorNames.append(name)

		# convert the L*a*b* array from the RGB color space
		# to L*a*b*
		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

	# Label each shape as winner or loser, based on its color...
	def label(self, image, c):
		# construct a mask for the contour, then compute the
		# average L*a*b* value for the masked region
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		mean = cv2.mean(image, mask=mask)[:3]

		# initialize the minimum distance found thus far
		minDist = (np.inf, None)

		# loop over the known L*a*b* color values
		for (i, row) in enumerate(self.lab):
			# compute the distance between the current L*a*b*
			# color value and the mean of the image
			d = distance.euclidean(row[0], mean)

			# if the distance is smaller than the current distance,
			# then update the bookkeeping variable
			if d < minDist[0]:
				minDist = (d, i)

		# return the name of the color with the smallest distance
		return self.colorNames[minDist[1]]

	# Write out edge detection and winner/loser labels to image file
	def write_out(self, image, cnts, lab):
		for c in cnts:
			# compute the center of the contour, then detect the name of the
			# shape using only the contour
			M = cv2.moments(c)

			# Get geometric center of shape; Does not count click mass within shape (i.e where most of the area is located)
			cX = int((M["m10"] / M["m00"]))
			cY = int((M["m01"] / M["m00"]))

			win_lose_tag = self.label(lab, c)

			# multiply the contour (x, y)-coordinates by the resize ratio,
			# then draw the contours and the winner/loser tag of the shape on the image
			c = c.astype("float")
			c = c.astype("int")
			center_tag =  str(cX) + ", " + str(cY)

			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			cv2.putText(image, win_lose_tag, (cX - 10, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)	# Draw win/lose tag
			cv2.putText(image, center_tag, (cX + 15, cY + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)	# Draw center coordinates
			cv2.circle(image, (cX, cY), 3, (255, 0, 255), -1)	# Draw circle at the center of shape

		# write the output image
		curr_time = str(datetime.datetime.now()).replace(":", ".")		# Remove restricted characters from time stamp
		filename = "click_maps/" + curr_time + " map" + str(self.map_number) + ".png"

		success = cv2.imwrite(filename, image)
		if success:
			print(datetime.datetime.now(), "Saved processed click map:", filename)
		else:
			print(datetime.datetime.now(), "Failed to save processed click map", filename)

		self.map_number += 1
		return

	# Return the center coordinates for the winner click location
	def find_winner_XY(self, cnts, lab):
		for c in cnts:
			if self.label(lab, c) == "winner":
				M = cv2.moments(c)
				cX = int((M["m10"] / M["m00"]))
				cY = int((M["m01"] / M["m00"]))
				return (cX, cY)
		return (-1, -1)

	# Fetch click map from URL, calculate the winner's x,y coordinate, save processes image(?)
	# THIS IS THE ONLY METHOD TO BE CALLED FROM THE MAIN MODULE
	def process_click_map(self, raw_image_data, doLogImage):

		np_arr = np.fromstring(raw_image_data, np.uint8)	# Convert png byte string to a numpy array
		cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)	# Have OpenCV load image from array

		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
		lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		if doLogImage:
			self.write_out(cv_image, cnts, lab)

		return self.find_winner_XY(cnts, lab)
