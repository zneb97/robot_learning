import os, sys
from os import path
import csv
import cv2 as cv
import numpy as np

csvfile = os.path.join("./data", 'ball_info.csv')

with open('ball_info.csv', mode='w') as ball_info:
    ball_writer = csv.writer(ball_info, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for filename in os.listdir("data"):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):

        base = cv.imread(filename)
        base = cv.resize(base, (320,240), interpolation = cv.INTER_AREA)
        img = cv.medianBlur(base.copy(),5)
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        lower = np.array([40, 10, 10])
        upper = np.array([110, 255, 255])

        img = cv.inRange(img, lower, upper)
        img = cv.erode(img, None, iterations=3)
        img = cv.dilate(img, None, iterations=2)

        contours = cv.findContours(img.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # Draw bounding circle around largest contour
        if len(contours) > 0:
            largest_contour = max(contours, key=cv.contourArea)
            ((x, y), radius) = cv.minEnclosingCircle(largest_contour)

            # Draw circles on image to represent the ball
            if radius > 10:
                cv.circle(base, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv.circle(base, (int(x), int(y)), 5,
                    (0, 0, 255), -1)
                print "coord:" + str(x) + "," + str(y) + " radius:" + str(radius)
                ball_writer.writerow(str(filename), str(x), str(y), str(radius)])
            else:
                print "Radius too small!"


        continue
    else:
        continue



cv.imshow('detected circles',base)
cv.waitKey(0)
cv.destroyAllWindows()
