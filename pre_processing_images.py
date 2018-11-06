import ballfinder as bf
import numpy as np
import os
import cv2 as cv


def turn_images_into_numpy_arrays(path, st_num, end_num):
    for i in range(st_num,(end_num+1):
        path_name = (path + "/"+string(i)+".png")
        image = cv.imread(path_name,,mode='RGB')
        
