"""
For each of the base images of the ball
near, mid, and far away, randomly generate
orientation and position along that axis to create
our training and validation set for our model
"""

from __future__ import division

from PIL import Image
import random, math
import csv

#Create and clear the top row of the csv file to store labels. The top row is cleared for headers
with open('/media/n4tticus/ZIEMANN1/Balls/ball_positions.csv', 'wb') as ball_positions:
	csv_write = csv.writer(ball_positions, quoting=csv.QUOTE_ALL)
	csv_write.writerow('')

#Generate 1000 images per ball y position
n = 0
while n < 3000:
	empty = Image.open('/media/n4tticus/ZIEMANN1/dataSet2/blank.jpg', 'r')
	empty_width, empty_height = empty.size

	#Generate the closest 1000 images
	if n < 1000:
		#Open the close ball file
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyClose.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 125 #Pixel value of top of ball
		max_angle = 30 #Maximum field of view
		distance = 70 #Distance to the ball if it is in the middle of the screen in inches
		max_horizontal = 40 #At the edge of the field of view, how many inches over is it
	#Generate the mid-range 1000 images
	elif n < 2000:
		#Open the middle ball file
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyMid.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 170
		max_angle = 30
		distance = 34
		max_horizontal = 20
	#Generate the farthest 1000 images
	else:
		#Open the farthest ball file
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyFar.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 180
		max_angle = 30
		distance = 12
		max_horizontal = 10

	#Offset is a tuple: (x coordinate, y coordinate) of top left corner of ball
	offset = (random.randint(0, 640 - ball_width), relative_height)
	
	#Randomly rotate the ball
	angle = random.randint(0, 360)
	ball = ball.rotate(angle)
	
	#Paste the rotated ball at the offset position within the empty image
	empty.paste(ball, offset, mask=ball)
	
	#Shrink the image to 160x120, exactly 1/4 the size of the original
	empty.thumbnail((160, 120), Image.ANTIALIAS)
	offset = (offset[0]/4, offset[1]/4)
	ball_width = ball_width/4
	ball_height = ball_height/4
	
	#Save the newly created image on the ZIEMANN1 drive
	empty.save('/media/n4tticus/ZIEMANN1/Balls/' + str(n) + '.png', format='png')
	
	#Iterate to next image
	n += 1

	#Store this line of label data in a csv so that it lines up with the training data
	with open('/media/n4tticus/ZIEMANN1/Balls/ball_positions.csv', 'a') as ball_positions:
		csv_write = csv.writer(ball_positions, quoting=csv.QUOTE_ALL)
		csv_write.writerow((offset[0], offset[1], offset[0] + ball_width, offset[1] + ball_height, 2*max_angle*(offset[0]/(640 - ball_width)) - max_angle, math.sqrt((2*max_horizontal*(offset[0]/(640 - ball_width)) - max_horizontal)**2 + distance**2)))
