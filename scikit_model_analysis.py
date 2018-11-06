"""
Offline version of the analysis of our keras model
using matplotlib to compare predicted vs expected
values for validation data set.
"""

import numpy as np
import os
import cv2
import pandas
import pickle
from tensorflow import keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

#Load the training and validation data. We will only be using the validation data from here, or 750 out of the 3000 images
data = np.load('/home/n4tticus/catkin_ws/robot_learning/balls5.npz')
print('data loaded')

#Load the saved scikit learn model, stored as a pkl file
model_sci = pickle.load(open('/home/n4tticus/catkin_ws/robot_learning/pickle_model.pkl', 'rb'))

#Grab the last 250 of each of the sets of 1000 images to use as validation data, the rest was used as training data for the model
val_images = np.append(np.append(data['arr_0'][750:1000], data['arr_0'][1750:2000]), data['arr_0'][2750:3000])

#Generate a new list of images and append all images to it
val_images_new = []
for i in range(val_images.shape[0]):
  val_images_new.append(val_images[i])

#Preprocess the validation images
val_images = preprocess_input(np.array(val_images_new))

#Load the image labels, stored as a csv. Only grab the angle column of the data, as this is the only column we care about in this model
labels = '/home/n4tticus/catkin_ws/robot_learning/ball_positions2.csv'
labels = (pandas.read_csv(labels))['angle']

#Grab the correct image labels that line up with the images we chose as validation data
val_labels_sci = np.append(np.append(labels[750:1000], labels[1750:2000]), labels[2750:3000])

#Cast these labels as integers, as they were previously floats
val_labels_sci = val_labels_sci.astype(int)

#Flatten the validation images from dimensions (750, 120, 160, 3) to (43200000, 1)
val_images_flattened = val_images.reshape((val_images.shape[0],
                                                  val_images.shape[1]*
                                                  val_images.shape[2]*
                                                  val_images.shape[3]))

#Use matplotlib to plot predicted and actual data to compare the two and check the accuracy of the model
plt.plot(model_sci.predict_log_proba(val_images_flattened)[:,1], label="predicted")
plt.plot(val_labels_sci, label="actual")
plt.legend()
plt.show()
