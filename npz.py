"""
Convert our data set into a numpy zip file
for uploading and use on Google Colaboratory
notebooks.
"""

import numpy as np
import cv2

#created  an empty array to store our images
images = np.empty((3000, 160, 120, 3), dtype=np.ndarray)

i=0
#itterate over our all pictures and turning them into an array
while i < 3000:
	temp_image = cv2.imread('/media/n4tticus/ZIEMANN1/Balls/' + str(i) + '.png')
	for j in range(0, 160):
		for k in range(0, 120):
			images[i][j][k] = np.array([temp_image[k][j][2], temp_image[k][j][1], temp_image[k][j][0]])
	i+=1

	if i%100 == 0:
		print(i)
#saving  that array
np.savez('/media/n4tticus/ZIEMANN1/balls.npz', images)


'''
images = np.empty(3000, dtype=np.ndarray)

for i in range(0, 3000):
	images[i] = cv2.imread('/media/n4tticus/ZIEMANN1/Balls/' + str(i) + '.png')

	if i%100 == 0:
		print(i)

np.savez('/media/n4tticus/ZIEMANN1/balls5.npz', images)
'''
#^^^ This is the code we actually ran. The other code was slow on google. 

newnpz = np.load('/media/n4tticus/ZIEMANN1/balls5.npz')
newarr = newnpz['arr_0']
print(newarr)
