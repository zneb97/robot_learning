from PIL import Image
import random, math

n = 0
while n < 3000:
	empty = Image.open('/media/n4tticus/ZIEMANN1/dataSet2/blank.jpg', 'r')
	empty_width, empty_height = empty.size

	if n < 1000:
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyClose.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 125
	elif n < 2000:
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyMid.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 170
	else:
		ball = Image.open('/media/n4tticus/ZIEMANN1/BallOnlyFar.png', 'r')
		ball_width, ball_height = ball.size
		relative_height = 180

	offset = (random.randint(0, 640 - ball_width), relative_height)
	angle = random.randint(0, 360)
	ball = ball.rotate(angle)
	empty.paste(ball, offset, mask=ball)
	empty.thumbnail((320, 240), Image.ANTIALIAS)
	empty.save('/home/n4tticus/Desktop/Balls/' + str(n) + '.png', format='png')
	n += 1