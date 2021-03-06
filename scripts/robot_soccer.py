#!/usr/bin/env python
"""
Turn the neato based on learned model
"""
import tensorflow as tf

import pandas
import math
import numpy as np
#from skimage.transform import resize
from PIL import Image as PImage
import matplotlib.pyplot as plt

import pickle
from tensorflow.keras.models import load_model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

import rospy
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge

from std_msgs.msg import String
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
from geometry_msgs.msg import Pose, Twist, Vector3
from nav_msgs.msg import Odometry

class RobotSoccer():

    def __init__(self):

        self.debugOn = False
        self.useSciModel = False
        self.imageFlag = 0
        self.vizImg = None

        #Robot properties
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linVector = Vector3(x=0.0, y=0.0, z=0.0)
        self.angVector = Vector3(x=0.0, y=0.0, z=0.0)
        self.kp = 1

        #Getting angle
        self.resize = (160, 120)
        self.ball_diameter = 7.5 #ball is 7.5 inches in diameter.
        self.fov = 60. #Field of view in degrees.
        self.focal = 150.*12./self.ball_diameter #The first number is the measured width in pixels of a picture taken at the second number's distance (inches).
        self.center = self.resize[0]/2

        #Image from pi camera
        self.img = None

        self.bridge = CvBridge()

        #ROS
        rospy.init_node('Robot_Soccer')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=2)
       
        self.rate = rospy.Rate(2)

        # rospy.Subscriber("/odom", Odometry, self.setLocation)

        if self.useSciModel:
            rospy.Subscriber("/camera/image_raw", Image, self.setImageSci)
        else:
            rospy.Subscriber('/camera/image_raw', Image, self.setImage)


    def publishVelocity(self, linX, angZ):
        """
        Publishes velocities to make the robot move

        linX is a floating point between 0 and 1 to control the robot's x linear velocity
        angZ is a floating point between 0 and 1 to control the robot's z angular velocity
        """
        if self.debugOn: print("publishing")

        self.linVector.x = linX
        self.angVector.z = angZ
        self.pub.publish(Twist(linear=self.linVector, angular=self.angVector))


    def setLocation(self, odom):
        """
        Convert pose (geometry_msgs.Pose) to a (x, y, theta) tuple
        Constantly being called as it is the callback function for this node's subscription

        odom is Neato ROS' nav_msgs/Odom msg composed of pose and orientation submessages
        """

        pose = odom.pose.pose
        orientation_tuple = (pose.orientation.x,
                                pose.orientation.y,
                                pose.orientation.z,
                                pose.orientation.w)
        angles = euler_from_quaternion(orientation_tuple)
        self.x = pose.position.x
        self.y = pose.position.y
        self.theta = angles[2]
        return (pose.position.x, pose.position.y, angles[2])


    def setImage(self, img):

        if self.imageFlag > 5:
            return

        img = self.bridge.imgmsg_to_cv2(img, desired_encoding="rgb8")
       # img = PImage.open(img)
        img = cv2.resize(img, (160, 120), interpolation=cv2.INTER_AREA)
        img = np.array(img)
        self.vizImg = img
        img = np.expand_dims(img, axis=0)
        print("Working!")
        self.img = img
        

        self.imageFlag +=1


    def setImageSci(self, img):

        if self.imageFlag > 5:
            return

        img = self.bridge.imgmsg_to_cv2(img, desired_encoding="rgb8")
       # img = PImage.open(img)
        img = cv2.resize(img, (160, 120), interpolation=cv2.INTER_AREA)
        
        img = np.array(img)
        img = img.reshape((img.shape[0]*img.shape[1]*img.shape[2]))
        img = np.expand_dims(img,axis=0)
        print(img.shape)
        self.img = img


    def trainThetaModel(self):
        """
        Train the model we will be using to move to the soccer ball
        This is based on feeding in an image with associtated angles of the ball
        and expecting it to return a theta heading

        labels - string file name of the .csv where labels are kept
        """

        #Training the model and dataset is now on Google Collabratory:
        #
        #Here we just read in the model from the generated model
        with open('sciModel.pkl', 'rb') as file:
            model = pickle.load(file)
            return model


    def getAngleDist(self, x, radius):
        angle = 60*(x/120) - 30
        distance = 2.3 - 1.9*radius/75
        return angle, distance


    def trainXYRModel(self):
        """
        Train the model we will be using to move to the soccer ball
        This is based on feeding in an image with associtated angles of the ball
        and expecting it to return xy_radius tuple
        """

        #Training the model and dataset is now on Google Collabratory:
        #
        #Here we just read in the model from the generated model
        model = tf.keras.models.load_model('kerasModel.h5')
        return model


    def turnToBall(self, ball_theta):
        """
        Turn the neato to the soccer ball based on the ball's relative location
        to the neato

        Depending on how theta is calculated may have to do some normalization
        """

        #Determine which way to turn.
        start_theta = self.theta
        ball_theta = -ball_theta
        if ball_theta > 1:
            angZ = 0.5
        elif ball_theta < -1:
            angZ = -0.5

        #Set angle to turn to
        goal_theta = ball_theta+self.theta

        if goal_theta > 360:
            goal_theta = goal_theta-360
        elif goal_theta < 0:
            goal_theta = goal_theta+360

        goal_theta = math.radians(goal_theta) - math.pi

        while(abs(self.theta-goal_theta) > .3):
            self.publishVelocity(0.0, angZ)
        self.publishVelocity(0.0, 0.0)


    def driveToBall(self, dist):
        start_pos = (self.x,self.y)
        currDist = dist
        while(currDist > .2):
            self.publishVelocity(0.1, 0.0)
            currDist = math.sqrt((start_pos[0]-self.x)**2 + (start_pos[1]-self.y)**2)
        self.publishVelocity(0.0, 0.0)


    def run(self):
        #Get the models
        if self.useSciModel:
            thetaModel = self.trainThetaModel()
        else:
            xyrModel = self.trainXYRModel()

        #Wait for first image to be obtained
        while(self.imageFlag < 5) and (not rospy.is_shutdown()):
            #print(self.imageFlag)
            continue

        if self.useSciModel:
            #This method is in the model file.
            ballTheta = thetaModel.predict(self.img)
        else:
            ballCoords = xyrModel.predict(self.img)
            print(ballCoords)
            ballCenter = int((ballCoords[0][2]-ballCoords[0][0])/2 + ballCoords[0][0])
            y = (ballCoords[0][3]-ballCoords[0][1])/2 + ballCoords[0][1]
            self.vizImg[int(y)][ballCenter] = (255,0,0)
            img = self.vizImg
            print(img.shape)
            plt.imshow(img)
            plt.show()
            radius = (ballCoords[0][2]-ballCoords[0][0])/2
            ballTheta, ballDist = self.getAngleDist(ballCenter, radius)
        print(ballTheta)

        self.turnToBall(ballTheta)
        self.driveToBall(ballDist)


if __name__ == "__main__":
  rs = RobotSoccer()
  rs.run()