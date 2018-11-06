from __future__ import division

from PIL import Image
import random, math
import csv

with open('/media/n4tticus/ZIEMANN1/Balls/ball_positions.csv', 'wb') as ball_positions:
	csv_write = csv.writer(ball_positions, quoting=csv.QUOTE_ALL)
	csv_write.writerow('')

n = 0
while n < 3000:
	empty = Image.open('/media/n4tticus/ZIEMANN1/dataSet2/blank.jpg', 'r')
	empty_width, empty_height = empty.size

	if n < 1000:
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyClose.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 125
		max_angle = 30
		distance = 70
		max_horizontal = 40
	elif n < 2000:
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyMid.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 170
		max_angle = 30
		distance = 34
		max_horizontal = 20
	else:
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyFar.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 180
		max_angle = 30
		distance = 12
		max_horizontal = 10

	offset = (random.randint(0, 640 - ball_width), relative_height)
	angle = random.randint(0, 360)
	ball = ball.rotate(angle)
	empty.paste(ball, offset, mask=ball)
	empty.thumbnail((160, 120), Image.ANTIALIAS)
	offset = (offset[0]/4, offset[1]/4)
	ball_width = ball_width/4
	ball_height = ball_height/4
	empty.save('/media/n4tticus/ZIEMANN1/Balls/' + str(n) + '.png', format='png')
	n += 1

	with open('/media/n4tticus/ZIEMANN1/Balls/ball_positions.csv', 'a') as ball_positions:
		csv_write = csv.writer(ball_positions, quoting=csv.QUOTE_ALL)
		csv_write.writerow((offset[0], offset[1], offset[0] + ball_width, offset[1] + ball_height, 2*max_angle*(offset[0]/(640 - ball_width)) - max_angle, math.sqrt((2*max_horizontal*(offset[0]/(640 - ball_width)) - max_horizontal)**2 + distance**2)))