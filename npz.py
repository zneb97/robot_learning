"""
Convert our data set into a numpy zip file
for uploading and use on Google Colaboratory
notebooks.
"""

import numpy as np
import cv2

#Create an empty numpy array of length 3000 to hold all of our images
images = np.empty(3000, dtype=np.ndarray)

#Iterate over the 3000 images and append them to the images list
for i in range(0, 3000):
	#Use openCV to read the images as numpy arrays of dimensions (120, 160, 3)
	images[i] = cv2.imread('/media/n4tticus/ZIEMANN1/Balls/' + str(i) + '.png')

	#Print the progress after every 100th image
	if i%100 == 0:
		print(i)

#Save the list of images in the compressed npz format
np.savez('/media/n4tticus/ZIEMANN1/balls5.npz', images)
print('npz created')

#To check that the images were loaded and saved correctly, attempt to load the newly created npz file and print the output
newnpz = np.load('/media/n4tticus/ZIEMANN1/balls5.npz')
newarr = newnpz['arr_0']
print(newarr)
