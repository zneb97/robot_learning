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
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.metrics import categorical_crossentropy, categorical_accuracy
from tensorflow.keras.layers import Flatten, Dense, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.activations import sigmoid
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.models import load_model

data = np.load('/home/n4tticus/catkin_ws/robot_learning/balls5.npz')

print('data loaded')

model = load_model('/home/n4tticus/catkin_ws/robot_learning/kerasModel.h5')

val_images = np.append(np.append(data['arr_0'][750:1000], data['arr_0'][1750:2000]), data['arr_0'][2750:3000])

val_images_new = []
for i in range(val_images.shape[0]):
  val_images_new.append(val_images[i])

val_images = preprocess_input(np.array(val_images_new))

labels = '/home/n4tticus/catkin_ws/robot_learning/ball_positions2.csv'

label_tlx = (pandas.read_csv(labels))['top left x']
label_tly = (pandas.read_csv(labels))['top left y']
label_brx = (pandas.read_csv(labels))['bottom right x']
label_bry = (pandas.read_csv(labels))['bottom right y']

#Format of [[x_min, y_min, x_max, y_max], [....], [....]]
labels_list = np.empty(len(label_tlx))
for i in range(len(label_tlx)):
  np.append(labels_list, np.array([label_tlx[i], label_tly[i], label_brx[i], label_bry[i]]))

#Split into training and validation data ratio 3:1
val_labels = np.append(np.append(label_tlx[750:1000], label_tlx[1750:2000]), label_tlx[2750:3000])

val_labels_predict = model.predict(val_images)

plt.hist(val_labels_predict, bins = 101, label='predicted')
plt.hist(val_labels, bins = 101, label='actual')
plt.legend()