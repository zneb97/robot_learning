import numpy as np
import cv2

images = np.empty(3000, dtype=np.ndarray)

i=0
while i < 3000:
	images[i] = cv2.imread('/media/n4tticus/ZIEMANN1/Balls/' + str(i) + '.png')
	i+=1

np.savez('/media/n4tticus/ZIEMANN1/balls.npz', images)
