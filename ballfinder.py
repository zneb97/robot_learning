import cv2 as cv
import numpy as np
base = cv.imread('testballcenter.jpg')
base = cv.resize(base, (320,240), interpolation = cv.INTER_AREA)
img = cv.medianBlur(base.copy(),5)
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lower = np.array([40, 10, 10])
upper = np.array([110, 255, 255])

img = cv.inRange(img, lower, upper)
img = cv.erode(img, None, iterations=3)
img = cv.dilate(img, None, iterations=2)


#todo: add in color filter.  Filter and create a binary image.

# circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
#                              param1=100,param2=100,minRadius=10,maxRadius=200)
#
# #Alt - Blob detection.
# if circles != None:
#     circles = np.uint16(np.around(circles))
#     for i in circles[0,:]:
#         # draw the outer circle
#         cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
#         # draw the center of the circle
#         cv.circle(img,(i[0],i[1]),2,(0,0,255),3)
# else: print "no circles scrub"

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
    else:
        print "Radius too small!"


cv.imshow('detected circles',base)
cv.waitKey(0)
cv.destroyAllWindows()
