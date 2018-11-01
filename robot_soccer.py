#!/usr/bin/env python
"""
Turn the neato based on learned model
"""

import rospy
import pandas
import math
import keras
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion, rotation_matrix, quaternion_from_matrix
from geometry_msgs.msg import Pose, Twist, Vector3
from nav_msgs.msg import Odometry
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

class RobotSoccer():

	def __init__(self):

		self.debugOn = Fasle

		#Robot properities
	    self.x = 0.0
	    self.y = 0.0
	    self.theta = 0.0
	    self.linVector = Vector3(x=0.0, y=0.0, z=0.0)
	    self.angVector = Vector3(x=0.0, y=0.0, z=0.0)

	    #ROS
	    self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=2)
	    rospy.init_node('tracePolygon')
	    self.rate = rospy.Rate(2)

	    rospy.Subscriber("/odom", Odometry, self.setLocation)
	    rospy.Subscriber("/camera_raw", Image, self.setImage)


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


	def setLocation(self):
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


   	def trainThetaModel(self, labels):
   		"""
		Train the model we will be using to move to the soccer ball
		This is based on feeding in an image with associtated angles of the ball
		and expecting it to return a theta heading

		labels - string file name of the .csv where labels are kept
   		"""

   		#Split the data 3:1 between training and validation
   		labels = (pandas.read_csv(labels))['theta']
   		train_labels = labels[0:int(len(labels)*.75)]
   		val_labels = labels[int(len(labels)*.75):len(labels)]

   		train_images = np.load('images/')[0:int(len(labels)*.75)]
   		train_images_prep = preprocess_input(train_images)
   		train_images_flattened = train_images_prep.reshape((train_images_prep.shape[0],
                                                    train_images_bump.prep[1]*
                                                    train_images_bump.prep[2]*
                                                    train_images_bump.prep[3]))

   		val_images = np.load('images/')[int(len(labels)*.75):len(labels)]
   		val_images_prep = preprocess_input(val_images)
   		val_images_flattened = val_images_prep.reshape((val_images_prep.shape[0],
                                                    val_images_bump.prep[1]*
                                                    val_images_bump.prep[2]*
                                                    val_images_bump.prep[3]))

   		#Train the model
   		model = LogisticRegression(C=.000001).fit(train_images_flattened, train_labels)

   		return model


   	def trainXYRModel(self, labels):
   		"""
		Train the model we will be using to move to the soccer ball
		This is based on feeding in an image with associtated angles of the ball
		and expecting it to return xy_radius tuple


   		"""
   		#Top left and bottom right coordinates of the bounding box
   		label_tlx = (pandas.read_csv(labels))['tlx']
   		label_tlx = (pandas.read_csv(labels))['tly']
   		label_tlx = (pandas.read_csv(labels))['brx']
   		label_tlx = (pandas.read_csv(labels))['bry']

   		train_labels_tlx = label_tlx[0:int(len(label_tlx)*.75)]
   		train_labels_tly = label_tlx[0:int(len(label_tly)*.75)]
   		train_labels_brx = label_tlx[0:int(len(label_brx)*.75)]
   		train_labels_bry = label_tlx[0:int(len(label_bry)*.75)]

   		val_labels_tlx = label_tlx[int(len(label_tlx)*.75):len(label_tlx)]
   		val_labels_tlx = label_tlx[int(len(label_tly)*.75):len(label_tly)]
   		val_labels_tlx = label_tlx[int(len(label_brx)*.75):len(label_brx)]
   		val_labels_tlx = label_tlx[int(len(label_bry)*.75):len(label_bry)]


   		train_images = np.load('images/')[0:int(len(label_tlx)*.75)]
   		train_images_prep = preprocess_input(train_images)
   		train_images_flattened = train_images_prep.reshape((train_images_prep.shape[0],
                                                    train_images_bump.prep[1]*
                                                    train_images_bump.prep[2]*
                                                    train_images_bump.prep[3]))

   		val_images = np.load('images/')[int(len(label_tlx)*.75):len(label_tlx)]
   		val_images_prep = preprocess_input(val_images)
   		val_images_flattened = val_images_prep.reshape((val_images_prep.shape[0],
                                                    val_images_bump.prep[1]*
                                                    val_images_bump.prep[2]*
                                                    val_images_bump.prep[3]))
   		
   		#KERAS MODEL HERE


   	def turnToBall(self, theta):
   		"""
		Turn the neato to the soccer ball based on the ball's relative location
		to the neato

		Depending on how theta is calculated may have to do some normalization
   		"""
   		start_theta = self.theta
   		self.publishVelocity(0.0,0.1)
   		while(start_theta < theta):
   			continue
   		self.publishVelocity(0.0,0.0)


   	def getBallAngle(self, x,y,r):
   		"""
		For the Keras model. Use the ball's x,y, and radius
		in the pi camera image to determine it's angle from
		the Neato
   		"""

   		return 0

   	def run(self):

