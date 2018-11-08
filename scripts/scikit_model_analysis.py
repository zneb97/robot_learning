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

data = np.load('/home/n4tticus/catkin_ws/robot_learning/balls5.npz')

print('data loaded')

model_sci = pickle.load(open('/home/n4tticus/catkin_ws/robot_learning/pickle_model.pkl', 'rb'))

val_images = np.append(np.append(data['arr_0'][750:1000], data['arr_0'][1750:2000]), data['arr_0'][2750:3000])

val_images_new = []
for i in range(val_images.shape[0]):
  val_images_new.append(val_images[i])

val_images = preprocess_input(np.array(val_images_new))

labels = '/home/n4tticus/catkin_ws/robot_learning/ball_positions2.csv'
labels = (pandas.read_csv(labels))['angle']

val_labels_sci = np.append(np.append(labels[750:1000], labels[1750:2000]), labels[2750:3000])
val_labels_sci = val_labels_sci.astype(int)

val_images_flattened = val_images.reshape((val_images.shape[0],
                                                  val_images.shape[1]*
                                                  val_images.shape[2]*
                                                  val_images.shape[3]))

plt.plot(model_sci.predict_log_proba(val_images_flattened)[:,1], label="predicted")
plt.plot(val_labels_sci, label="actual")
plt.legend()
plt.show()